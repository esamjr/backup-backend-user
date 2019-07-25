from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from registrations.models import Register
from business_account.models import Business
import time
import json
import requests

# Create your views here.
@api_view(['GET','POST','PUT'])
def pilih_sku(request):
	try :
		token = request.META.get('HTTP_AUTHORIZATION')
		user = Register.objects.get(token = token)
		comp = Business.objects.get(id_user = user.id)
		if request.method == 'GET':
			if settings.FLAG == 0:
				url = 'http://dev-billing-api.mindzzle.com/sku/api/all/'
			elif settings.FLAG == 1:
				url = 'https://billing-api.mindzzle.com/sku/api/all/'
			elif settings.FLAG == 2:
				url = 'http://staging-billing-api.mindzzle.com/sku/api/all/'
			elif settings.FLAG == 3:
				url = 'http://127.0.0.1:8888/sku/api/all/'
			Req = requests.get(url)
			Res = Req.json()
			return Response(Res)

		elif request.method == 'POST':
			if settings.FLAG == 0:
				url = 'http://dev-billing-api.mindzzle.com/pomanagment/api/detail/post/'
			elif settings.FLAG == 1:
				url = 'https://billing-api.mindzzle.com/pomanagment/api/detail/post/'
			elif settings.FLAG == 2:
				url = 'http://staging-billing-api.mindzzle.com/pomanagment/api/detail/post/'
			elif settings.FLAG == 3:
				url = 'http://127.0.0.1:8888/pomanagment/api/detail/post/'

			payload = {
			'id_sku' : request.data['id_sku'],
			'qty' : request.data['qty'],
			'po_id' : request.data['po_id'],
			'company_id' : comp.id,
			'currency' : request.data['currency']
			}

			Req = requests.post(url, data = payload)
			Res = Req.json()
			return Response(Res)

		elif request.method == 'PUT':
			if settings.FLAG == 0:
				url = 'http://dev-billing-api.mindzzle.com/pomanagment/api/'
			elif settings.FLAG == 1:
				url = 'https://billing-api.mindzzle.com/pomanagment/api/'
			elif settings.FLAG == 2:
				url = 'http://staging-billing-api.mindzzle.com/pomanagment/api/'
			elif settings.FLAG == 3:
				url = 'http://127.0.0.1:8888/pomanagment/api/'

			payload = {
			'comp_id' : comp.id,
			'id_tax' : request.data['id_tax'],
			'discount_id' : request.data['discount_id'],
			'aggrement_id' : request.data['aggrement_id'],
			'no_po' : request.data['no_po'],
			'description' : request.data['description'],
			'status_po' : request.data['status_po'],
			'status' : request.data['status'],
			'user_id' : user.id
			}
			Req1 = requests.post(url, data = payload)
			Res1 = Req1.json()
			return Response(Res1)
	except Register.DoesNotExist:
		return Response({'status':'User Does Not Exist'})
	except Business.DoesNotExist:
		return Response({'status':'You are not Company Admin'})