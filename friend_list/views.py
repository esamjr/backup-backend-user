from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import friendlist
from .serializers import FriendlistSerializer
from django.db.models import Q
import json


@api_view(['GET', 'DELETE', 'PUT'])

def get_delete_update_friendlist(request, pk):
    try:
        Friend_list = friendlist.objects.all().filter(Q(id_user_from=pk)|Q(id_user_to=pk))
    except Friend_list.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':        
        serializer = FriendlistSerializer(Friend_list, many=True)
        return Response(serializer.data)

  
@api_view(['GET', 'POST'])

def get_post_friendlist(request):
    if request.method == 'GET':
        network = friendlist.objects.all()
        serializer = FriendlistSerializer(network, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = FriendlistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
