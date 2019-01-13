from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Region as Private
from .serializers import PrivateSerializer
import json

@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_typetime(request, pk):
    try:
        region = Private.objects.get(pk=pk)
    except Region.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PrivateSerializer(region)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if(request.user == region.name):
            region.delete()
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
        if(request.user == region.name):
            serializer = PrivateSerializer(user_type, data=request.data)
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
def get_post_typetime(request):
    if request.method == 'GET':
        network = Private.objects.all()
        serializer = PrivateSerializer(network, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PrivateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_post_typetime_user(request,pk):
    if request.method == 'GET':
        network = Private.objects.all().filter(id_user=pk)
        serializer = PrivateSerializer(network, many=True)
        return Response(serializer.data)