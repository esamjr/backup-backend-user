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
			i = 1
			for idh in hirarki:				
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
					result[idh] = str(i) + '. Error input pada id hirarki : '+str(idh)
					i = i+1
					# return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
			return Response(result, status = status.HTTP_201_CREATED)
		elif request.method == 'PUT':
			hirarki = Hierarchy.objects.get(id = pk)
			beacon = jobdesc.objects.get(id_hierarchy = hirarki.id)
			payload = {
			'id_comp':beacon.id_comp,
			'id_hierarchy': beacon.id_hierarchy,
			'desc':request.data['desc']
			}
			serializer = JobdescSerialiser(beacon, data = payload)
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
