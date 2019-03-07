from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Jobcontract as Job_contract
from .serializers import JobcontractSerializer

@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_jobcontract(request, pk):
    try:
        Jobcontract = Job_contract.objects.get(pk=pk)
    except Job_contract.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = JobcontractSerializer(Jobcontract)
        return Response(serializer.data)

    elif request.method == 'DELETE':       
            
            content = {
                'status' : 'NO CONTENT'
            }
            Jobcontract.delete()
            return Response(content, status=status.HTTP_204_NO_CONTENT)
       
    elif request.method == 'PUT':
       
            serializer = JobcontractSerializer(Jobcontract, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
@api_view(['GET', 'POST'])
def get_post_jobcontract(request):
    if request.method == 'GET':
        network = Job_contract.objects.all()
        serializer = JobcontractSerializer(network, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = JobcontractSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_jobcontract(request, pk1):
    try:
        network = Job_contract.objects.all().filter(id_company = pk1)
        serializer = JobcontractSerializer(network, many=True)
        return Response(serializer.data)
    except Job_contract.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    