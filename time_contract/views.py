from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Timecontract as Time_contract
from .serializers import TimecontractSerializer

@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_timecontract(request, pk):
    try:
        Timecontract = Time_contract.objects.get(pk=pk)
    except Time_contract.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    Timecontract = Time_contract.objects.get(pk=pk)
    if request.method == 'GET':
        serializer = TimecontractSerializer(Timecontract)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if(request.user == Timecontract.name):
            Timecontract.delete()
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
        if(request.user == Timecontract.name):
            serializer = TimecontractSerializer(Timecontract, data=request.data)
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
def get_post_timecontract(request):
    if request.method == 'GET':
        network = Time_contract.objects.all()
        serializer = TimecontractSerializer(network, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TimecontractSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_timecontract(request, pk):
    try:
        network = Time_contract.objects.all().filter(id_company=pk)
        serializer = TimecontractSerializer(network, many=True)
        return Response(serializer.data)
    except Time_contract.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)