from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import goal_negotiation
from .serializers import GoalnegoSerializer

@api_view(['GET','POST','PUT','DELETE'])
def goal_nego(request):
	if request.method == 'POST':
		serializers = GoalnegoSerializer(data = request.data)
		if serializers.is_valid():
			serializers.save()
			return Response(serializers.data, status=status.HTTP_201_CREATED)
		return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
	elif request.method == 'GET':
		netw = goal_negotiation.objects.all()
		serializers = GoalnegoSerializer(netw, many = True)
		return Response(serializers.data, status=status.HTTP_201_CREATED)
	elif request.method == 'PUT':
		try:
			idx = request.data['id']
			beacon = goal_negotiation.objects.get(id = idx)
			serializers = GoalnegoSerializer(beacon, data = request.data)
			if serializers.is_valid():
				serializers.save()
				return Response(serializers.data, status=status.HTTP_201_CREATED)
			return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
		except goal_negotiation.DoesNotExist:
			response = {'status':'GOAL NEGOTIATION DOES NOT EXIST'}
			return Response(response, status=status.HTTP_400_BAD_REQUEST)
	elif request.method == 'DELETE':
		try:
			idx = request.data['id']
			beacon = goal_negotiation.objects.get(id=idx)
			beacon.delete()
			response = {'status':'DELETION SUCCESSFULL'}
			return Response(response, status = status.HTTP_204_NO_CONTENT)
		except goal_negotiation.DoesNotExist:
			response = {'status':'GOAL NEGOTIATION DOES NOT EXIST'}
			return Response(response, status=status.HTTP_404_NOT_FOUND)
