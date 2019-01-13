from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Joincompany
from .serializers import JoincompanySerializer

@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_joincompany(request, pk):
    try:
        join_company = Joincompany.objects.get(pk=pk)
    except Joincompany.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = JoincompanySerializer(join_company)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if(request.user == Joincompany):
            join_company.delete()
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
        if(request.user == Joincompany):
            serializer = JoincompanySerializer(Joincompany, data=request.data)
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
def get_post_joincompany(request):
    if request.method == 'GET':
        network = Joincompany.objects.all()
        serializer = JoincompanySerializer(network, many=True)
        return Response(serializer.data)

  
    elif request.method == 'POST':
        serializer = JoincompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_post_joincompany_user(request,pk):
    if request.method == 'GET':
        network = Joincompany.objects.all().filter(id_user=pk)
        serializer = JoincompanySerializer(network, many=True)
        return Response(serializer.data)
