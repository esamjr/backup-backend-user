from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import review_scheduler
from .serializers import ReviewSerializer

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def revies_sched(request):
	if request.method == 'POST':
		serializers = ReviewSerializer(data = request.data)
		if serializers.is_valid():
			serializers.save()
			return Response(serializers.data, status=status.HTTP_201_CREATED)
		return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)
	elif request.method == 'GET':
		netw = revies_scheduler.objects.all()
		serializers = ReviewSerializer(netw, many=True)
		return Response(serializers.data, status=status.HTTP_201_CREATED)
	elif request.method == 'PUT':
		try:
			idx = request.data['id']
			beacon = review_scheduler.objects.get(id = idx)
			serializers = ReviewSerializer(beacon, data = request.data)
			if serializers.is_valid():
				serializers.save()
				return Response(serializers.data, status=status.HTTP_201_CREATED)
			return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
		except review_scheduler.DoesNotExist:
			response = {'status':'DATA DOES NOT EXIST'}
			return Response(response, status=status.HTTP_400_BAD_REQUEST)
	elif request.method == 'DELETE':
		try:
			idx = request.data['id']
			beacon = review_scheduler.objects.get(id = idx)
			beacon.delete()
			response = {'status':'DELETION SUCCSESS'}
			return Response(response, status=HTTP_204_NO_CONTENT)
		except review_scheduler.DoesNotExist:
			response = {'status':'DATA DOES NOT EXIST'}
			return Response(response, status=status.HTTP_400_BAD_REQUEST)