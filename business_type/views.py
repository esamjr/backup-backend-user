from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Businesstype as Bussiness_type
from .serializers import BusinesstypeSerializer

@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_businesstype(request, pk):
    try:
        Businesstype = Bussiness_type.objects.get(pk=pk)
    except Businesstype.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = BusinesstypeSerializer(Businesstype)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if(request.user == Businesstype):
            Businesstype.delete()
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
        if(request.user == Businesstype):
            serializer = BusinesstypeSerializer(Businesstype, data=request.data)
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
def get_post_businesstype(request):
    if request.method == 'GET':
        network = Bussiness_type.objects.all()
        serializer = BusinesstypeSerializer(network, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BusinesstypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_businesstype(request,pk):
    try:
        network = Bussiness_type.objects.all().filter(id_company=pk)
        serializer = BusinesstypeSerializer(network, many=True)
        return Response(serializer.data)
    except Bussiness_type.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)