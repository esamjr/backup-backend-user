from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Typetime as Time_type
from .serializers import TypetimeSerializer

@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_typetime(request, pk):
    try:
        Typetime = Time_type.objects.get(pk=pk)
    except Typetime.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = TypetimeSerializer(Typetime)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if(request.user == Typetime):
            Typetime.delete()
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
        if(request.user == Typetime):
            serializer = TypetimeSerializer(user_type, data=request.data)
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
        network = Time_type.objects.all()
        serializer = TypetimeSerializer(network, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TypetimeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)