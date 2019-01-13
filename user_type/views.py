from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Usertype
from .serializers import UsertypeSerializer

@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_usertype(request, pk):
    try:
        user_type = Usertype.object.get(pk=pk)
    except Usertype.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = Usertypeserializer(user_type)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if(request.user == user_type.name):
            user_type.delete()
            content = {
                'status' : 'NO CONTENT'
            }
            return Response(content, status=status.HTTP_202_NO_CONTENT)
        else:
            content = {
                'status' : 'UNAUTHORIZED'
            }
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)
    elif request.method == 'PUT':
        if(request.user == user_type.name):
            serializer = UsertypeSerializer(user_type, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            content = {
                'status': 'UNAUTHORIZED'
            }
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET', 'POST'])
def get_post_usertype(request):
    if request.method == 'GET':
        network = Usertype.objects.all()
        serializer = UsertypeSerializer(network, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UsertypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)