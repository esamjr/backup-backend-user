from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Level as Level_models
from .serializers import LevelSerializer

@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_level(request, pk):
    try:
        Level = Level_models.objects.get(pk=pk)
    except Level_models.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = LevelSerializer(Level_models)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if(request.user == Level_models):
            Level.delete()
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
        if(request.user == Level_models):
            serializer = LevelSerializer(Level_models, data=request.data)
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
def get_post_level(request):
    if request.method == 'GET':
        network = Level_models.objects.all()
        serializer = LevelSerializer(network, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = LevelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def filter_comp(request, pk):
    if request.method == 'POST':        

        try:
            id_comp = Level_models.objects.get(id_company = pk)
            network = LevelSerializer(id_comp)
            return(network.data)
        except Level_models.DoesNotExist:
            return Response([], status = status.HTTP_404_NOT_FOUND)


