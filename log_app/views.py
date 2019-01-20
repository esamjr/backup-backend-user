from django.shortcuts import render
from .serializers import LoggingSerializer
from .models import Logging
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
import time

@api_view(['GET'])
def Logview(request):
    network = Logging.objects.all()
    serializer = LoggingSerializer(network, many=True)
    return Response(serializer.data)

@csrf_exempt
def create_log(request, modelDB, act):
	db = modelDB
	times = time.asctime(time.localtime(time.time()))
	executors = db.full_name
	activities = act + executors
	payload = {
		'date_time' : times,
		'executor' : executors,
		'activity' : activities,
		'vendor' : None
		}
	connection = LoggingSerializer(data = payload)
	if connection.is_valid():
		connection.save()
		response = {'Log created'}
		return HttpResponse(response, status = status.HTTP_201_CREATED)
	else:
		response = {'Failed to create log'}
		return HttpResponse(response, status = status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def read_log(request, modelDB, act):
	db = modelDB
	times = time.asctime(time.localtime(time.time()))
	executors = db.full_name
	activities = act + executors
	payload = {
		'date_time' : times,
		'executor' : executors,
		'activity' : activities,
		'vendor' : None
		}
	connection = LoggingSerializer(data = payload)
	if connection.is_valid():
		connection.save()
		response = {'Log created'}
		return HttpResponse(response, status = status.HTTP_201_CREATED)
	else:
		response = {'Failed to create log'}
		return HttpResponse(response, status = status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def update_log(request, modelDB, act):
	db = modelDB
	times = time.asctime(time.localtime(time.time()))
	executors = db.full_name
	activities = act + executors
	payload = {
		'date_time' : times,
		'executor' : executors,
		'activity' : activities,
		'vendor' : None
		}
	connection = LoggingSerializer(data = payload)
	if connection.is_valid():
		connection.save()
		response = {'Log created'}
		return HttpResponse(response, status = status.HTTP_201_CREATED)
	else:
		response = {'Failed to create log'}
		return HttpResponse(response, status = status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def delete_log(request, modelDB, deleteDB, act):
	db = modelDB
	times = time.asctime(time.localtime(time.time()))
	executors = modelDB.full_name
	activities = act + deleteDB + 'by' + executors
	payload = {
		'date_time' : times,
		'executor' : executors,
		'activity' : activities,
		'vendor' : None
		}
	connection = LoggingSerializer(data = payload)
	if connection.is_valid():
		connection.save()
		response = {'Log created'}
		return HttpResponse(response, status = status.HTTP_201_CREATED)
	else:
		response = {'Failed to create log'}
		return HttpResponse(response, status = status.HTTP_400_BAD_REQUEST)



# debug code
 # try: 
 #                            serializer = CertificationSerializer(Certification)
 #                            dbase = registrations
 #                            times = time.asctime(time.localtime(time.time()))
 #                            executors = dbase.full_name
 #                            activities = 'read by '+ executors
 #                            payload = {
 #                                'date_time' : times,
 #                                'executor' : executors,
 #                                'activity' : activities,
 #                                'vendor' : None
 #                                }
 #                        except:
 #                            response = {'Failed to create lo x'}
 #                            return HttpResponse(response, status=status.HTTP_400_BAD_REQUEST)
                            
 #                        connection = LoggingSerializer(data = payload)
 #                        if connection.is_valid():
 #                            connection.save()
 #                            response = {'Log created'}
 #                            return Response(response, status = status.HTTP_201_CREATED)
 #                        else:
 #                            response = {'Failed to create log'}
 #                            return Response(connection.errors, status=status.HTTP_400_BAD_REQUEST)