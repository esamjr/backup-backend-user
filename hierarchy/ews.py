from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Hierarchy as hirarki
from .serializers import HierarchySerializer

@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_hierarchy(request, pk):
    try:
        Hierarchy = hirarki.objects.get(pk=pk)
    except Hierarchy.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = HierarchySerializer(Hierarchy)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if(request.user == Hierarchy):
            Hierarchy.delete()
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
        if(request.user == Hierarchy):
            serializer = HierarchySerializer(Hierarchy, data=request.data)
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
def get_post_hierarchy(request):
    if request.method == 'GET':
        network = hirarki.objects.all()
        serializer = HierarchySerializer(network, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = HierarchySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()#name==request.user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

       