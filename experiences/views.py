from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Experiences as pengalaman
from .serializers import ExperiencesSerializer
from registrations.models import Register

@api_view(['GET','DELETE', 'PUT'])

def get_delete_update_experiences(request, pk):
    try:
        Experiences = pengalaman.objects.get(pk=pk)
        registrations = Register.objects.get(pk=pk)
        if (registrations.token == 'xxx'):
            response = {'status':'LOGIN FIRST, YOU MUST...'}
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        else:    
            try:
                token = request.META.get('HTTP_AUTHORIZATION','')
                get_token = Register.objects.get(token = token)
                if (get_token.id == Experiences.id):

                    if request.method == 'GET':
                        serializer = ExperiencesSerializer(Experiences)
                        return Response(serializer.data)

                    elif request.method == 'DELETE':
                        if (Experiences == "0"):                    
                            Experiences.delete()
                            content = {
                                'status' : 'NO CONTENT'
                            }
                            return Response(content, status=status.HTTP_202_NO_CONTENT)
                        else:
                            content = {'status':'Cannot touch this, because your experience already verified'}
                            return Response(content, status=status.HTTP_401_UNAUTHORIZED)
                    elif request.method == 'PUT':                
                        serializer = ExperiencesSerializer(Experiences, data=request.data)
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
    except pengalaman.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST'])
def get_post_experiences(request):
    if request.method == 'GET':
        network = pengalaman.objects.all()
        serializer = ExperiencesSerializer(network, many=True)
        return Response(serializer.data)


    elif request.method == 'POST':
        serializer = ExperiencesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_post_experiences_user(request,pk):
   
    try:
        if request.method == 'GET':
            network = pengalaman.objects.all().filter(id_user=pk)
            serializer = ExperiencesSerializer(network, many=True)
            return Response(serializer.data)
    except pengalaman.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)



