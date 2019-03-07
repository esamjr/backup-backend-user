from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import CertificationBA
from registrations.models import Register
from .serializers import CertificationBASerializer
from log_app.views import create_log, read_log, update_log, delete_log
from log_app.serializers import LoggingSerializer
from log_app.models import Logging
import time

@api_view(['GET','DELETE', 'PUT'])
def get_delete_update_certification(request, pk):
    try:
        Certification = CertificationBA.objects.get(pk=pk)
        registrations = Register.objects.get(pk=Certification.id_user)
        if (registrations.token == 'xxx'):
            response = {'status':'LOGIN FIRST, YOU MUST...'}
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        else:    
            try:
                token = request.META.get('HTTP_AUTHORIZATION','')
                get_token = Register.objects.get(token = token)
                if (get_token.id == Certification.id_user):
                    if request.method == 'GET':                        
                        serializer = CertificationBASerializer(Certification) 
                        act = 'Read certification by '                           
                        read_log(request, registrations,act)
                        return Response(serializer.data)

                    elif request.method == 'DELETE':
                        if (Certification.verified == "0"):                                                    
                            act = 'Delete certification by id : '                           
                            delete_log(request, registrations, Certification.CertificationBA_name, act)                                
                            Certification.delete()
                            content = {
                                'status' : 'NO CONTENT'
                            }
                            return Response(content, status=status.HTTP_204_NO_CONTENT)
                            
                        else:
                            content = {'status':'Cannot touch this, Your Ceritification is already verified' }
                            return Response(content, status=status.HTTP_401_UNAUTHORIZED)
                        
                    elif request.method == 'PUT':
                       
                            serializer = CertificationBASerializer(Certification, data=request.data)
                            if serializer.is_valid():
                                serializer.save()
                                act = 'Update certification by '
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
                    'status': 'Not Found user'
                }
                return Response(content, status=status.HTTP_404_NOT_FOUND)

    except CertificationBA.DoesNotExist:
        content = {
            'status': 'Not Found CertificationBA'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST'])

def get_post_certification(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    registrations = Register.objects.get(token =token)
    if request.method == 'GET':
        network = CertificationBA.objects.all()
        serializer = CertificationBASerializer(network, many=True)
        act = 'Read all certification by '                           
        read_log(request, registrations,act)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CertificationBASerializer(data=request.data)
        if serializer.is_valid(): 
            serializer.save()#sementara dihilangkan dulu parameter (Certification.id_user==request.user)
            act = 'Create new certification by '
            create_log(request, registrations, act)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])

def get_post_certification_user(request,pk):
    if request.method == 'GET':
        token = request.META.get('HTTP_AUTHORIZATION')
        registrations = Register.objects.get(token =token)
        try:        
            network = CertificationBA.objects.all().filter(id_user=pk)
            serializer = CertificationBASerializer(network, many=True)
            act = 'Read certification by '                           
            read_log(request, registrations,act)
            return Response(serializer.data)
        except CertificationBA.DoesNotExist:
            content = {
                'status': 'Not Found'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
