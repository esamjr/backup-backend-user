from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Goal
from .serializers import GoalSerializer

@api_view(['POST, GET'])
def post_get_goals(request):
	if request.method == 'POST':
		return
	elif request.method == 'GET':
		return

@api_view(['GET','PUT','DELETE'])
def get_put_delete(request,pk):
	if request.method == 'GET':
		return
	elif request.method == 'PUT':
		return
	elif request.method == 'DELETE':
		return
		