from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Experiences as pengalaman
from .serializers import ExperiencesSerializer
from registrations.models import Register
from log_app.views import create_log, read_log, update_log, delete_log
from log_app.serializers import LoggingSerializer
from log_app.models import Logging
from business_account.models import Business
import time

@api_view(['GET','DELETE', 'PUT'])

def get_delete_update_experiences(request, pk):
    try:
        Experiences = pengalaman.objects.get(id=pk)
        company = Business.objects.get(id = Experiences.id_company).id_user
        registrations = Register.objects.get(id=Experiences.id_user)
        if (registrations.token == 'xxx'):
            response = {'status':'LOGIN FIRST, YOU MUST...'}
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        else:    
            try:
                token = request.META.get('HTTP_AUTHORIZATION','')
                get_token = Register.objects.get(token = token)
                if ((get_token.id == Experiences.id_user) | (get_token.id == company)):
                    if request.method == 'GET':
                        serializer = ExperiencesSerializer(Experiences)
                        act = 'Read experience by '                           
                        read_log(request, registrations,act)
                        return Response(serializer.data)

                    elif request.method == 'DELETE':
                        if (Experiences.verified == "0"):                    
                            Experiences.delete()
                            act = 'Delete experience by id : '                           
                            delete_log(request, registrations, Experiences.position, act)
                            content = {
                                'status' : 'NO CONTENT'
                            }
                            return Response(content, status=status.HTTP_201_CREATED)
                        else:
                            content = {'status':'Cannot touch this, because your experience already verified'}
                            return Response(content, status=status.HTTP_401_UNAUTHORIZED)
                    elif request.method == 'PUT':                
                        serializer = ExperiencesSerializer(Experiences, data=request.data)
                        if serializer.is_valid():
                            serializer.save()
                            act = 'Update experience by '
                            update_log(request, registrations, act)
                            return Response(serializer.data, status=status.HTTP_201_CREATED)
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                else:
                    content = {
                    'status': 'UNAUTHORIZED'
                    }
                    return Response(content, status=status.HTTP_401_UNAUTHORIZED)
                
            except Register.DoesNotExist:
                content = {
                    'status': 'Not found in register'
                }
                return Response(content, status=status.HTTP_404_NOT_FOUND)
    except pengalaman.DoesNotExist:
        content = {
            'status': 'Not Found in Experience'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST'])
def get_post_experiences(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    registrations = Register.objects.get(token =token)
    if request.method == 'GET':
        network = pengalaman.objects.all()
        serializer = ExperiencesSerializer(network, many=True)
        act = 'Read all experience by '                           
        read_log(request, registrations,act)
        return Response(serializer.data)


    elif request.method == 'POST':
        serializer = ExperiencesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            act = 'Create new experience by '
            create_log(request, registrations, act)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_post_experiences_user(request,pk):
    token = request.META.get('HTTP_AUTHORIZATION')
    registrations = Register.objects.get(token =token)
    try:
        if request.method == 'GET':
            network = pengalaman.objects.all().filter(id_user=pk)
            serializer = ExperiencesSerializer(network, many=True)
            act = 'Read experience by '                           
            read_log(request, registrations,act)
            return Response(serializer.data)
    except pengalaman.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)



