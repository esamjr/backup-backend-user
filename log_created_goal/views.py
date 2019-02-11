from django.shortcuts import render
from .serializers import LogGoalSerializer,LogGoalUpdateSerializer
from .models import log_goal
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
import time
@csrf_exempt
def create_log_goal(request, id_company,id_goal,id_hierarchy,id_user):
	times = time.asctime(time.localtime(time.time()))
	payload = {'id_company': id_company,
				'id_goal':id_goal,
				'id_hierarchy':id_hierarchy,
				'id_user':id_user,
				'created_at':times}
	serializers = LogGoalSerializer(data = payload)
	if serializers.is_valid():
		serializers.save()
		return Response(serializers.data)
	return Response(serializers.errors)

@csrf_exempt
def update_log_goal(request, id_company,id_goal,id_hierarchy,id_user):
	times = time.asctime(time.localtime(time.time()))
	beacon = log_goal.objects.get(id_company = id_company, id_goal= id_goal, id_hierarchy=id_hierarchy, id_user = id_user)
	payload = {'update_at':times}
	serializers = LogGoalUpdateSerializer(beacon, data = payload)
	if serializers.is_valid():
		serializers.save()
		return Response(serializers.data)
	return Response(serializers.errors)