from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Task
from .serializers import TaskSerializer

@api_view(['GET','POST'])
def get_post(request):
	try :
		if request.method == 'GET':
			beacon = Task.objects.all()
			serializer = TaskSerializer(beacon, many = True)
			return Response(serializer.data, status = status.HTTP_200_OK)
		elif request.method == 'POST':
			serializer = TaskSerializer(data = request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status = status.HTTP_201_CREATED)
			return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
	except Task.DoesNotExist:
		return Response({'status':'Task Does Not Exist'})

@api_view(['GET','PUT','DELETE'])
def get_put_delete(request, pk):
	try:
		if request.method == 'GET':
			beacon = Task.objects.get(id = pk)
			serializer = TaskSerializer(beacon)
			return Response(serializer.data, status = status.HTTP_200_OK)
		elif request.method == 'PUT':
			beacon = Task.objects.get(id = pk)
			serializer = TaskSerializer(beacon, data = request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status = status.HTTP_200_OK)
			return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
		elif request.method == 'DELETE':
			beacon = Task.objects.get(id = pk)
			beacon.delete()
			return Response({'status':'Successfull ! '}, status = status.HTTP_200_OK)
	except Task.DoesNotExist:
		return Response({'status':'Task Does Not Exist'})

@api_view(['POST'])
def report_task_perday(request):
	day = request.data['DD']
	id_comp = request.data['id_comp']
	result = []
	if day == '':
		beacon = Task.objects.all().filter(id_company = id_comp)
		serializer = TaskSerializer(beacon, many = True)
		return Response(serializer.data)
	elif id_comp == '':
		beacon = Task.objects.all()
		for obj in beacon:
			deadline = duedate
			if deadline[8:] == day:
				serializer = TaskSerializer(ojb)
				result.append(serializer.data)
			else:
				pass
		return Response(result)
	else:
		beacon = Task.objects.all().filter(id_company = id_comp)
		for obj in beacon:
			deadline = duedate
			if deadline[8:] == day:
				serializer = TaskSerializer(ojb)
				result.append(serializer.data)
			else:
				pass
		return Response(result)
