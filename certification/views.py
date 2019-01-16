from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Certification as certificate
from registrations.models import Register
from .serializers import CertificationSerializer
from .permissions import IsOwnerOrReadOnly

@api_view(['GET', 'DELETE', 'PUT'])

def get_delete_update_certification(request, pk):
    try:
        Certification = certificate.objects.get(pk=pk)
        try:
            token = request.META.get('HTTP_AUTHORIZATION','')
            get_token = Register.objects.get(token = token)
            if (get_token.id == Certification.id):
                if request.method == 'GET':
                    serializer = CertificationSerializer(Certification)
                    return Response(serializer.data)

                elif request.method == 'DELETE':
                    if(request.user == Certification):
                        Certification.delete()
                        content = {
                            'status' : 'NO CONTENT'
                        }
                        return Response(content, status=status.HTTP_201_CREATED)
                    
                elif request.method == 'PUT':
                   
                        serializer = CertificationSerializer(education, data=request.data)
                        if serializer.is_valid():
                            serializer.save()
                            return Response(serializer.data, status=status.HTTP_201_CREATED)
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                content = {
                'status': 'UNAUTHORIZED'
                }
                return Response(content, status=status.HTTP_401_UNAUTHORIZED)
    
        except Register.DoesNotExist:
            content = {
                'status': 'UNAUTHORIZED'
            }
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)

    except certificate.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST'])

def get_post_certification(request):
    if request.method == 'GET':
        network = certificate.objects.all()
        serializer = CertificationSerializer(network, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CertificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()#sementara dihilangkan dulu parameter (Certification.id_user==request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])

def get_post_certification_user(request,pk):
    if request.method == 'GET':
        try:        
            network = certificate.objects.all().filter(id_user=pk)
            serializer = CertificationSerializer(network, many=True)
            return Response(serializer.data)
        except certificate.DoesNotExist:
            content = {
                'status': 'Not Found'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
