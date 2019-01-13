from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Employeesign
from .serializers import EmployeesignSerializer

@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_employeesign(request, pk):
    try:
        employee_sign = Employeesign.objects.get(pk=pk)
    except Employeesign.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = EmployeesignSerializer(employee_sign)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if(request.user == employee_sign):
            employee_sign.delete()
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
        if(request.user == employee_sign):
            serializer = EmployeesignSerializer(employee_sign, data=request.data)
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
def get_post_employeesign(request):
    if request.method == 'GET':
        network = Employeesign.objects.all()
        serializer = EmployeesignSerializer(network, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EmployeesignSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def get_all_employeesign(request, pk1, pk2):
    try:
        network = Employeesign.objects.all().filter(id_company=pk1 )
        serializer = EmployeesignSerializer(network, many=True)
        return Response(serializer.data)
    except Employeesign.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)
