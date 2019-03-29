from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Historyhierarchy
from .serializers import HistoryhierarchySerializer
from registrations.models import Register

@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_historyhierarchy(request, pk):
    try:
        history_hierarchy = Historyhierarchy.objects.get(pk=pk)
    except Historyhierarchy.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        
        serializer = HistoryhierarchySerializer(history_hierarchy)
        users = Register.objects.get(id = serializer.data['id_user'])

        return Response({'nama':users.name,'data':serializer.data})

    elif request.method == 'DELETE':
        
            history_hierarchy.delete()
            content = {
                'status' : 'NO CONTENT'
            }
      
    elif request.method == 'PUT':
        
            serializer = HistoryhierarchySerializer(history_hierarchy, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      

@api_view(['GET', 'POST'])
def get_post_historyhierarchy(request):
    if request.method == 'GET':
        network = Historyhierarchy.objects.all()        
        datas = []
        for nets in network:
            serializer = HistoryhierarchySerializer(nets)
            sets = {'nama':users.name,'data':serializer.data}
            datas.append(sets)
        return Response(datas)

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
        return Response(content, status=status.HTTP_404_NOT_FOUND)
