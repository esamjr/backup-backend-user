from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import type_goal
from .serializers import TypegoalSerializer

@api_view(['POST','GET','PUT', 'DELETE'])
def tipe_goal(request):
	if request.method == 'POST':
		serializer = TypegoalSerializer(data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status = status.HTTP_201_CREATED)
		return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

	elif request.method == 'GET':
		netw = type_goal.objects.all()
		serializer = TypegoalSerializer(netw, many = True)
		return Response(serializer.data, status = status.HTTP_201_CREATED)

	elif request.method == 'PUT':
		try:
			idx = request.data['id']
			beacon = type_goal.objects.get(id=idx)
			serializer = TypegoalSerializer(beacon, data = request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		except type_goal.DoesNotExist:
			response = {'status': 'NOT FOUND'}
			return Response(response, status=status.HTTP_404_NOT_FOUND)

	elif request.method == 'DELETE':
		try:
			idx = request.data['id']
			beacon = type_goal.objects.get(id=idx)
			beacon.delete()
			response = {'status':'DELETION SUCCSESS'}
			return Response(response, status=status.HTTP_201_CREATED)
		except type_goal.DoesNotExist:
			response = {'status': 'NOT FOUND'}
			return Response(response, status=status.HTTP_404_NOT_FOUND)





