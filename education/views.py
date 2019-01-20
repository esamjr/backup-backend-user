from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Education as pendidikan
from .serializers import EducationSerializer
from registrations.models import Register
from log_app.views import create_log, read_log, update_log, delete_log
from log_app.serializers import LoggingSerializer
from log_app.models import Logging
import time

@api_view(['GET','DELETE', 'PUT'])

def get_delete_update_education(request, pk):
    try:
        Education = pendidikan.objects.get(pk=pk)
        registrations = Register.objects.get(pk=Education.id_user)
        if (registrations.token == 'xxx'):
            response = {'status':'LOGIN FIRST, YOU MUST...'}
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        else:    
            try:
                token = request.META.get('HTTP_AUTHORIZATION','')
                get_token = Register.objects.get(token = token)
                if (get_token.id == Education.id_user):
                    if request.method == 'GET':
                        serializer = EducationSerializer(Education)
                        act = 'Read education by '                           
                        read_log(request, registrations,act)
                        return Response(serializer.data)

                    elif request.method == 'DELETE':
                        if (Education.verified == "0"):
                            act = 'Delete education by id : '                           
                            delete_log(request, registrations, Education.level, act)
                            Education.delete()
                            content = {
                                'status' : 'NO CONTENT'
                            }
                            return Response(content, status=status.HTTP_201_CREATED)
                        else:
                            content = {'status':'Cannot touch this, because your education info already verified'}
                            return Response(content, status=status.HTTP_401_UNAUTHORIZED)
                        
                    elif request.method == 'PUT':                
                            serializer = EducationSerializer(Education, data=request.data)
                            if serializer.is_valid():
                                serializer.save()
                                act = 'Update education by '
                                update_log(request, registrations, act)
                                return Response(serializer.data, status=status.HTTP_201_CREATED)
                            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    # if request.method == 'GET':
                    #     serializer = EducationSerializer(Education)
                    #     return Response(serializer.data)
                  
                else:
                    content = {
                    'status': 'UNAUTHORIZED'
                    }
                    return Response(content, status=status.HTTP_401_UNAUTHORIZED)
            except Register.DoesNotExist:
                content = {
                    'status': 'NOT FOUND in register'
                }
                return Response(content, status=status.HTTP_404_NOT_FOUND)
    except Education.DoesNotExist:
        content = {
            'status': 'Not Found in education'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST'])
def get_post_education(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    registrations = Register.objects.get(token =token)
    if request.method == 'GET':
        network = pendidikan.objects.all()
        serializer = EducationSerializer(network, many=True)
        act = 'Read all education by '                           
        read_log(request, registrations,act)
        return Response(serializer.data)


    elif request.method == 'POST':
        serializer = EducationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            act = 'Create new education by '
            create_log(request, registrations, act)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_post_education_user(request,pk):
    token = request.META.get('HTTP_AUTHORIZATION')
    registrations = Register.objects.get(token =token)
    try:
        if request.method == 'GET':
            network = pendidikan.objects.all().filter(id_user=pk)
            serializer = EducationSerializer(network, many=True)
            act = 'Read education by '                           
            read_log(request, registrations,act)
            return Response(serializer.data)
    except pendidikan.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    
