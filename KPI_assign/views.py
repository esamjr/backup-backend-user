from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import kpi_assign
from .serializers import KpiAssignSerializer

@api_view(['GET','POST'])
def get_post(request):
	try:
		if request.method == 'GET':
			beacon = kpi_assign.objects.all()
			serializer = KpiAssignSerializer(beacon, many = True)
			return Response(serializer.data, status = status.HTTP_200_OK)
		elif request.method == 'POST':
			serializer = KpiAssignSerializer(data = request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status = status.HTTP_201_CREATED)
			return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
	except kpi_assign.DoesNotExist:
		return Response({'status':'object Does Not Exist'})

@api_view(['GET','PUT','DELETE'])
def get_put_delete(request, pk):
	try:
		if request.method == 'GET':
			beacon = kpi_assign.objects.get(id = pk)
			serializer = KpiAssignSerializer(beacon)
			return Response(serializer.data, status = status.HTTP_200_OK)
		elif request.method == 'PUT':
			beacon = kpi_assign.objects.get(id = pk)
			serializer = KpiAssignSerializer(beacon, data = request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status = status.HTTP_200_OK)
			return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
		elif request.method == 'DELETE':
			beacon = kpi_assign.objects.get(id = pk)
			beacon.delete()
			return Response({'status':'Successfull ! '}, status = status.HTTP_200_OK)
	except kpi_assign.DoesNotExist:
		return Response({'status':'object Does Not Exist'})
