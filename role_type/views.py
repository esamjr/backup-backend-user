from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Roletype as Role_type
from .serializers import RoletypeSerializer

@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_roletype(request, pk):
    try:
        Roletype = Role_type.object.get(pk=pk)
    except Role_type.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)

    Roletype = Role_type.object.get(pk=pk)
    if request.method == 'GET':
        serializer = Roletypeserializer(Roletype)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if(request.user == Roletype.name):
            Roletype.delete()
            content = {
                'status' : 'NO CONTENT'
            }
            return Response(content, status=status.HTTP_204_NO_CONTENT)
        else:
            content = {
                'status' : 'UNAUTHORIZED'
            }
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)
    elif request.method == 'PUT':
        if(request.user == Roletype):
            serializer = RoletypeSerializer(Roletype, data=request.data)
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
def get_post_roletype(request):
    if request.method == 'GET':
        network = Role_type.objects.all()
        serializer = Roletype(network, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RoletypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)