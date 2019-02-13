from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Joincompany
from registrations.models import Register
from .serializers import JoincompanySerializer

@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_joincompany(request, pk):
    try:
        token = request.META.get('HTTP_AUTHORIZATION')
        user = Register.objects.get(token=token)
    except Register.DoesNotExist:
        content = {
            'status': 'UNAUTHORIZED'
        }
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)

    join_company = Joincompany.objects.get(id = pk)        
    if request.method == 'GET':
        serializer = JoincompanySerializer(join_company)
        return Response(serializer.data)
    elif request.method == 'DELETE':        
            join_company.delete()
            content = {
                'status' : 'EXTERMINATE...EXTERMINATE...'
            }
            return Response(content, status=status.HTTP_202_NO_CONTENT)        
    elif request.method == 'PUT':      
            serializer = JoincompanySerializer(join_company, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
  
    try:
        if request.method == 'GET':
            network = Joincompany.objects.all().filter(id_user=pk)
            serializer = JoincompanySerializer(network, many=True)
            return Response(serializer.data)
   
    except Joincompany.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)
