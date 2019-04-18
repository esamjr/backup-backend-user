from django.shortcuts import render
from .serializers import JobdescSerialiser
from .models import jobdesc
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from business_account.models import Business
from hierarchy.models import Hierarchy
import time

@api_view(['POST','PUT', 'GET'])
def automigrate_hierarchy_to_jobdesc(request, pk):
	try:
		if request.method == 'POST':
			company = Business.objects.get(id = pk)
			hirarki = Hierarchy.objects.all().values_list('id', flat = True).filter(id_company = company.id)
			result = {}
			for idh in hirarki:
				i = 0
				payload = {
				'id_hierarchy': idh,
				'desc':'Input Your Description Here'
				}
				serializer = JobdescSerialiser(data = payload)
				if serializer.is_valid():
					serializer.save()
					result[idh] = serializer.data
					# return Response(serializer.data, status =status.HTTP_201_CREATED)
				else:
					result[idh] = 'Error input pada id hirarki : '+str(idh)
					# return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
			return Response(result, status = status.HTTP_201_CREATED)
		elif request.method == 'PUT':
			hirarki = Hierarchy.objects.get(id = pk)
			beacon = jobdesc.objects.get(id_hierarchy = hirarki.id)			
			serializer = JobdescSerialiser(beacon, data = request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status = status.HTTP_200_OK)
			return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
		elif request.method == 'GET':
			beacon = jobdesc.objects.get(id = pk)
			serializer = JobdescSerialiser(beacon)
			return Response(serializer.data, status = status.HTTP_200_OK)
			
	except jobdesc.DoesNotExist:
		return Response({'status' : 'Job Description Does Not Exist, Please input your company Jobs Descriptions'}, status = status.HTTP_404_NOT_FOUND)
	except Business.DoesNotExist:
		return Response({'status' : 'Company Does Not Exist'}, status = status.HTTP_404_NOT_FOUND)
	except Hierarchy.DoesNotExist:
		return Response({'status' : 'Hierarchy Does Not Exist, Please Create The Hierarchy First'}, status = status.HTTP_404_NOT_FOUND)



# @api_view(['GET'])
# def Logview(request):
#     network = Logging.objects.all()
#     serializer = LoggingSerializer(network, many=True)
#     return Response(serializer.data)

# @csrf_exempt
# def create_log(request, modelDB, act):
# 	db = modelDB
# 	times = time.asctime(time.localtime(time.time()))
# 	executors = db.full_name
# 	activities = act + executors
# 	payload = {
# 		'date_time' : times,
# 		'executor' : executors,
# 		'activity' : activities,
# 		'vendor' : None
# 		}
# 	connection = LoggingSerializer(data = payload)
# 	if connection.is_valid():
# 		connection.save()
# 		response = {'Log created'}
# 		return HttpResponse(response, status = status.HTTP_201_CREATED)
# 	else:
# 		response = {'Failed to create log'}
# 		return HttpResponse(response, status = status.HTTP_400_BAD_REQUEST)

# @csrf_exempt
# def read_log(request, modelDB, act):
# 	db = modelDB
# 	times = time.asctime(time.localtime(time.time()))
# 	executors = db.full_name
# 	activities = act + executors
# 	payload = {
# 		'date_time' : times,
# 		'executor' : executors,
# 		'activity' : activities,
# 		'vendor' : None
# 		}
# 	connection = LoggingSerializer(data = payload)
# 	if connection.is_valid():
# 		connection.save()
# 		response = {'Log created'}
# 		return HttpResponse(response, status = status.HTTP_201_CREATED)
# 	else:
# 		response = {'Failed to create log'}
# 		return HttpResponse(response, status = status.HTTP_400_BAD_REQUEST)

# @csrf_exempt
# def update_log(request, modelDB, act):
# 	db = modelDB
# 	times = time.asctime(time.localtime(time.time()))
# 	executors = db.full_name
# 	activities = act + executors
# 	payload = {
# 		'date_time' : times,
# 		'executor' : executors,
# 		'activity' : activities,
# 		'vendor' : None
# 		}
# 	connection = LoggingSerializer(data = payload)
# 	if connection.is_valid():
# 		connection.save()
# 		response = {'Log created'}
# 		return HttpResponse(response, status = status.HTTP_201_CREATED)
# 	else:
# 		response = {'Failed to create log'}
# 		return HttpResponse(response, status = status.HTTP_400_BAD_REQUEST)

# @csrf_exempt
# def delete_log(request, modelDB, deleteDB, act):
# 	db = modelDB
# 	times = time.asctime(time.localtime(time.time()))
# 	executors = modelDB.full_name
# 	activities = act + deleteDB + 'by' + executors
# 	payload = {
# 		'date_time' : times,
# 		'executor' : executors,
# 		'activity' : activities,
# 		'vendor' : None
# 		}
# 	connection = LoggingSerializer(data = payload)
# 	if connection.is_valid():
# 		connection.save()
# 		response = {'Log created'}
# 		return HttpResponse(response, status = status.HTTP_201_CREATED)
# 	else:
# 		response = {'Failed to create log'}
# 		return HttpResponse(response, status = status.HTTP_400_BAD_REQUEST)



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