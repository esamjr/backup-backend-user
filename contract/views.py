from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Contract
from .serializers import contractSerializer

@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_contract(request, pk):
    try:
        contract = Contract.objects.get(pk=pk)
    except Contract.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = contractSerializer(contract)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if(request.user == contract):
            contract.delete()
            content = {
                'status' : 'NO CONTENT'
            }
            return Response(content, status=status.HTTP_204_NO_CONTENT)
        else:
            content = {
                'status' : 'UNAUTHORIZED'
            }
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)
    elif request.method == 'PUT':
        if(request.user == contract):
            serializer = contractSerializer(contract, data=request.data)
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
def get_post_contract(request):
    if request.method == 'GET':
        network = Contract.objects.all()
        serializer = contractSerializer(network, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = contractSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def get_all_contract(request,pk):
    try:
        network = Contract.objects.all().filter(id_company=pk)
        serializer = contractSerializer(network, many=True)
        return Response(serializer.data)
    except Contract.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)
