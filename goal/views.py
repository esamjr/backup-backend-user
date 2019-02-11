from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Goal
from .serializers import GoalSerializer
from type_goal.serializers import TypegoalSerializer
from type_goal.models import type_goal
from review_scheduler.serializers import ReviewSerializer
from review_scheduler.models import review_scheduler
from log_created_goal.views import create_log_goal, update_log_goal

@api_view(['POST', 'GET'])
def post_get_goals(request):
	if request.method == 'POST':
		serializers = GoalSerializer(data = request.data)
		if serializers.is_valid():
			serializers.save()
			create_log_goal(request, serializers.data['id_company'],serializers.data['id'],serializers.data['id_hierarchy'],serializers.data['id_user'])
			return Response(serializers.data, status = status.HTTP_201_CREATED)
		return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)
	elif request.method == 'GET':
		netw = Goal.objects.all()
		serializer = GoalSerializer(netw, many = True)
		return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET','PUT','DELETE'])
def get_put_delete(request,pk):
	try:
		beacon = Goal.objects.get(id=pk)
		if request.method == 'GET':
			tipe = type_goal.objects.get(id = beacon.id_type_goal)
			serializer1 = TypegoalSerializer(tipe)
			sched = review_scheduler.objects.get(id = beacon.id_review_scheduler)
			serializer2 = ReviewSerializer(sched)
			payload = {
				'id_company' : beacon.id_company,
				'title' : beacon.title,
				'description' : beacon.description,
				'parent' : beacon.parent,
				'parent_goal' : beacon.parent_goal,
				'id_hierarchy' : beacon.id_hierarchy,
				'id_type_goal' : serializer1.data,
				'mox_jobdesk' : beacon.mox_jobdesk,
				'max_bonus' : beacon.max_bonus,
				'status' : beacon.status,
				'id_review_scheduler' : serializer2.data,
				'id_level' : beacon.id_level,
				'time_allocation' : beacon.time_allocation,
				'sisa_allocation' : beacon.sisa_allocation
			}
			return Response(payload, status = status.HTTP_201_CREATED)
		elif request.method == 'PUT':
			serializer = GoalSerializer(beacon, data = request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)		
		elif request.method == 'DELETE':
			beacon.delete()
			response = {'status':'DELETION SUCCESS'}
			return Response(response, status=status.HTTP_204_NO_CONTENT)
	except Goal.DoesNotExist:
		response={'status' : 'GOAL DOES NOT EXIST'}
		return Response(response, status=status.HTTP_404_NOT_FOUND)
