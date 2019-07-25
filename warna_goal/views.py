from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import warna_goal
from .serializers import WarnaGaolSerializer

@api_view(['GET','POST'])
def get_post(request):
	try:
		if request.method == 'GET':
			beacon = warna_goal.objects.all()
			serializer = WarnaGaolSerializer(beacon, many = True)
			return Response(serializer.data, status = status.HTTP_200_OK)
		elif request.method == 'POST':
			serializer = WarnaGaolSerializer(data = request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status = status.HTTP_201_CREATED)
			return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
	except warna_goal.DoesNotExist:
		return Response({'status':'Goals Color Does Not Exist'})

@api_view(['GET','PUT','DELETE'])
def get_put_delete(request, pk):
	try:
		if request.method == 'GET':
			beacon = warna_goal.objects.get(id = pk)
			serializer = WarnaGaolSerializer(beacon)
			return Response(serializer.data, status = status.HTTP_200_OK)
		elif request.method == 'PUT':
			beacon = warna_goal.objects.get(id = pk)
			serializer = WarnaGaolSerializer(beacon, data = request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status = status.HTTP_200_OK)
			return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
		elif request.method == 'DELETE':
			beacon = warna_goal.objects.get(id = pk)
			beacon.delete()
			return Response({'status':'Successfull ! '}, status = status.HTTP_200_OK)
	except warna_goal.DoesNotExist:
		return Response({'status':'Goals Color Does Not Exist'})