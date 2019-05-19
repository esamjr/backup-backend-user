from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from registrations.models import Register
from django.conf import settings
import requests
import json

# Create your views here.
@api_view(['GET','POST','PUT','DELETE'])
def api_haloarif(request, string):
	if request.method == 'POST':
		if string == 'register':
			if settings.FLAG == 1:
				url = 'http://halloarif.org/api/v1/sign_up?'
			else:
				url = 'http://halloarif.org/api/v1/sign_up?'
			email = 'user[email]='+request.data['email']
			phone = '&user[phone_number]='+request.data['phone_number']
			full_name ='&user[full_name]='+request.data['full_name']
			referall = '&user[signup_referral_code]'+request.data['referal']
			password = '&user[password]='+request.data['password']
			password_confirm = '&user[password_confirmation]='+request.data['password_confirmation']
			Req = requests.post(url+email+phone+full_name+referall+password+password_confirm)
			Res = Req.json()
			return Response(Res)
		elif string == 'login':
			if settings.FLAG == 1:
				url = 'http://halloarif.org/api/v1/sign_in?'
			else:
				url = 'http://halloarif.org/api/v1/sign_in?'
			# sign_in[email]=mayangsari@mailinator&sign_in[password]=asd123
			email = 'sign_in[email]='+request.data['email']
			password = '&sign_in[password]='+request.data['password']
			Req = requests.post(url+email+password)
			Res = Req.json()
			return Response(Res)
		elif string == 'createmessage':
			# --------------------Work In Progress----------------------
			if settings.FLAG == 1:
				url = 'http://halloarif.org/api/v1/message_boxes'
			else:
				url = 'http://halloarif.org/api/v1/sign_up?'
			url_refrence = 'http://halloarif.org//list-category.json'
			req_ref = requests.get(url_refrence)
			res_ref = req_ref.json()
			data = res_ref['data']

			# token = request.data['token_arif']
			# header = {'AUTH-TOKEN':token}

			# Req = requests.post(url+email+phone+full_name+referall+password+password_confirm)
			# Res = Req.json()
			return Response(data)
		else:
			return Response({'status':'Endpoint Is Invalid'}, status = status.HTTP_400_BAD_REQUEST)
	elif request.method == 'GET':
		if string == 'getboxes':
			if settings.FLAG == 1:
				url = 'http://halloarif.org/api/v1/message_boxes/'
			else:
				url = 'http://halloarif.org/api/v1/message_boxes/'

			token = request.data['token_arif']
			header = {'AUTH-TOKEN':token}
			Req = requests.get(url, headers = header)
			Res = Req.json()
			return Response(Res)
		elif string == 'getboxessub':			
			if settings.FLAG == 1:
				url = 'http://halloarif.org/api/v1/message_boxes/14'
			else:
				url = 'http://halloarif.org/api/v1/message_boxes/14'

			token = request.data['token_arif']
			header = {'AUTH-TOKEN':token}
			Req = requests.get(url, headers = header)
			Res = Req.json()
			return Response(Res)
	elif request.method == 'PUT':
		if string == 'updateId':
			if settings.FLAG == 1:
				url = 'http://halloarif.org/api/v1/update_identity'
			else:
				url = 'http://halloarif.org/api/v1/update_identity'
			
			token = request.data['token_arif']
			header = {'AUTH-TOKEN':token}
			payload = {
			'range_age' : request.data['user[range_age]'],
			'gender' : request.data['user[gender]'],
			'martial_stat' : request.data['user[marital_status]'],
			'occupation' : request.data['user[occupation]'],
			'province' : request.data['user[province_id]'],
			'city':request.data['user[city_id]']
			}
			Req = requests.put(url, headers = header, data = payload)
			Res = Req.json()
			return Response(Res)
		elif string == 'logout':
			if settings.FLAG == 1:
				url = 'http://halloarif.org/api/v1/log_out'
			else:
				url = 'http://halloarif.org/api/v1/log_out'
						
			Req = requests.delete(url)
			Res = Req.json()
			return Response(Res)
