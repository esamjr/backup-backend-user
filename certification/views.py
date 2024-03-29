from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from log_app.views import read_log, update_log, delete_log
from registrations.models import Register
from .models import Certification as certificate
from .serializers import CertificationSerializer


@api_view(['GET','DELETE', 'PUT'])
def get_delete_update_certification(request, pk):
    try:
        Certification = certificate.objects.get(pk=pk)
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
                        serializer = CertificationSerializer(Certification) 
                        act = 'Read certification by '                           
                        read_log(request, registrations,act)
                        return Response(serializer.data)

                    elif request.method == 'DELETE':
                        if (Certification.verified == "0"):                                                    
                            act = 'Delete certification by id : '                           
                            delete_log(request, registrations, Certification.certificate_name, act)                                
                            Certification.delete()
                            content = {
                                'status' : 'NO CONTENT'
                            }
                            return Response(content, status=status.HTTP_204_NO_CONTENT)
                            
                        else:
                            content = {'status':'Cannot touch this, Your Ceritification is already verified' }
                            return Response(content, status=status.HTTP_401_UNAUTHORIZED)
                        
                    elif request.method == 'PUT':
                       
                            serializer = CertificationSerializer(Certification, data=request.data)
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

    except certificate.DoesNotExist:
        content = {
            'status': 'Not Found certificate'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def get_post_certification(request):
    try:
        if request.method == 'GET':
            network = certificate.objects.all()
            serializer = CertificationSerializer(network, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = CertificationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()  # sementara dihilangkan dulu parameter (Certification.id_user==request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Register.DoesNotExist:
        content = {
            'status': 'Not Found certificate'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def get_post_certification_user(request,pk):
    if request.method == 'GET':
        token = request.META.get('HTTP_AUTHORIZATION')
        registrations = Register.objects.get(token =token)
        try:        
            network = certificate.objects.all().filter(id_user=pk)
            serializer = CertificationSerializer(network, many=True)
            act = 'Read certification by '                           
            read_log(request, registrations,act)
            return Response(serializer.data)
        except certificate.DoesNotExist:
            content = {
                'status': 'Not Found'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
