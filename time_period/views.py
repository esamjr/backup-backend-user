from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import time_period
from .serializers import TimeSerializer

@api_view(['GET','POST'])
def get_post(request):
	if request.method == 'GET':
		beacon = time_period.objects.all()
		serializer = TimeSerializer(beacon, many = True)
		return Response(serializer.data, status = status.HTTP_200_OK)
	elif request.method == 'POST':
		serializer = TimeSerializer(data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status = status.HTTP_201_CREATED)
		return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def get_put_delete(request, pk):
	if request.method == 'GET':
		beacon = time_period.objects.get(id = pk)
		serializer = TimeSerializer(beacon)
		return Response(serializer.data, status = status.HTTP_200_OK)
	elif request.method == 'PUT':
		beacon = time_period.objects.get(id = pk)
		serializer = TimeSerializer(beacon, data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status = status.HTTP_200_OK)
		return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
	elif request.method == 'DELETE':
		beacon = time_period.objects.get(id = pk)
		beacon.delete()
		return Response({'status':'Successfull ! '}, status = status.HTTP_200_OK)


# @api_view(['GET','POST','PUT','DELETE'])
# def goal_assignment(request):
# 	if request.method == 'POST':
# 		serializers = GoalassignSerializer(data = request.data)
# 		if serializers.is_valid():
# 			serializers.save()
# 			return Response(serializers.data, status=status.HTTP_201_CREATED)
# 		return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
# 	elif request.method == 'GET':
# 		netw = Goal_assign.objects.all()
# 		serializers = GoalassignSerializer(netw, many = True)
# 		return Response(serializers.data, status=status.HTTP_201_CREATED)
# 	elif request.method == 'PUT':
# 		try:
# 			idx = request.data['id']
# 			beacon = Goal_assign.objects.get(id = idx)
# 			serializers = GoalassignSerializer(beacon, data = request.data)
# 			if serializers.is_valid():
# 				serializers.save()
# 				return Response(serializers.data, status=status.HTTP_201_CREATED)
# 			return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
# 		except Goal_assign.DoesNotExist:
# 			response = {'status':'GOAL ASSIGN DOES NOT EXIST'}
# 			return Response(response, status=status.HTTP_400_BAD_REQUEST)
# 	elif request.method == 'DELETE':
# 		try:
# 			idx = request.data['id']
# 			beacon = Goal_assign.objects.get(id=idx)
# 			bea()con.delete
# 			response = {'status':'DELETION SUCCESSFULL'}
# 			return Response(response, status = status.HTTP_204_NO_CONTENT)
# 		except Goal_assign.DoesNotExist:
# 			response = {'status':'GOAL ASSIGNMENT DOES NOT EXIST'}
# 			return Response(response, status=status.HTTP_404_NOT_FOUND)