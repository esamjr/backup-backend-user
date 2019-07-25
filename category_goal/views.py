from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import cat_goal
from .serializers import CatGoalSerializer

@api_view(['GET','POST'])
def get_post_catgoal(request):
	try:
		if request.method == 'GET':
			beacon = cat_goal.objects.all()
			serializer = CatGoalSerializer(beacon, many = True)
			return Response(serializer.data, status = status.HTTP_200_OK)
		elif request.method == 'POST':
			serializer = CatGoalSerializer(data = request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status = status.HTTP_201_CREATED)
			return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
	except cat_goal.DoesNotExist:
		return Response({'status':'Category Does Not Exist'})

@api_view(['GET','PUT','DELETE'])
def get_put_delete(request, pk):
	try:
		if request.method == 'GET':
			beacon = cat_goal.objects.get(id = pk)
			serializer = CatGoalSerializer(beacon)
			return Response(serializer.data, status = status.HTTP_200_OK)
		elif request.method == 'PUT':
			beacon = cat_goal.objects.get(id = pk)
			serializer = CatGoalSerializer(beacon, data = request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status = status.HTTP_200_OK)
			return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
		elif request.method == 'DELETE':
			beacon = cat_goal.objects.get(id = pk)
			beacon.delete()
			return Response({'status':'Successfull ! '}, status = status.HTTP_200_OK)
	except cat_goal.DoesNotExist:
		return Response({'status':'Category Does Not Exist'})