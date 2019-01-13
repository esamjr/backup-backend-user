from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Historyhierarchy
from .serializers import HistoryhierarchySerializer

@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_historyhierarchy(request, pk):
    try:
        history_hierarchy = Historyhierarchy.objects.get(pk=pk)
    except Historyhierarchy.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_401_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = HistoryhierarchySerializer(history_hierarchy)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if(request.user == history_hierarchy):
            history_hierarchy.delete()
            content = {
                'status' : 'NO CONTENT'
            }
            return Response(content, status=status.HTTP_202_NO_CONTENT)
        else:
            content = {
                'status' : 'UNAUTHORIZED'
            }
            return Response(content, status=status.HTTP_404_UNAUTHORIZED)
    elif request.method == 'PUT':
        if(request.user == history_hierarchy):
            serializer = HistoryhierarchySerializer(Joincompany, data=request.data)
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
def get_post_historyhierarchy(request):
    if request.method == 'GET':
        network = Historyhierarchy.objects.all()
        serializer = HistoryhierarchySerializer(network, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = HistoryhierarchySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_historyhierarchy(request, pk):
    try:
        network = Historyhierarchy.objects.all().filter(id_company=pk)
        serializer = HistoryhierarchySerializer(network, many=True)
        return Response(serializer.data)
    except Historyhierarchy.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_401_NOT_FOUND)
