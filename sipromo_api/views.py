from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from registrations.models import Register
import requests
import json
# Create your views here.

@api_view(['POST'])
def sipromo(request, stri):
	if stri =='get_vouchers':
		url = 'https://api.sipromo.id/get/vouchers'
		header = {'Content-Type':'application/json'}
		payload = {
		'appToken':'$2y$10$KMWlIAhy6p8gGPJx7tdgKOOgAIksjaaB6ZLUXWYtKxJH.9m/9oTy6',
		'appID':'92771509'
		}
		Req = requests.post(url, headers= header, data = payload)
		Res = Res.json()
	elif stri == 'get_voucher_detail':
		url = 'https://api.sipromo.id/get/voucher_detail'
		header = {'Content-Type':'application/json'}
		payload = {
		'appToken': '$2y$10$KMWlIAhy6p8gGPJx7tdgKOOgAIksjaaB6ZLUXWYtKxJH.9m/9oTy6',
		'appID': '92771509',
		'voucher_id': request.data['voucher_id']
		}
		Req = requests.post(url, headers = header, data = payload)
		Res = Req.json()
	elif stri == 'redeem_voucher':
		token = request.META.get('HTTP_AUTHORIZATION')
		user = Register.objects.get(token = token)
		url = 'https://api.sipromo.id/redeem'
		header = {'Content-Type':'application/json'}
		payload = {
		'appToken': '$2y$10$KMWlIAhy6p8gGPJx7tdgKOOgAIksjaaB6ZLUXWYtKxJH.9m/9oTy6',
		'appID': '92771509',
		'voucher_id': request.data['voucher_id'],
		'user_id': user.id
		}
		Req = requests.post(url, headers = header, data = payload)
		Res = Req.json()
	elif stri == 'get_user_voucher_redeem':
		token = request.META.get('HTTP_AUTHORIZATION')
		user = Register.objects.get(token = token)
		url = 'https://api.sipromo.id/get/user_voucher/redeem'
		header = {'Content-Type':'application/json'}
		payload = {
		'appToken': '$2y$10$KMWlIAhy6p8gGPJx7tdgKOOgAIksjaaB6ZLUXWYtKxJH.9m/9oTy6',
		'appID': '92771509',
		'user_id': user.id
		}
		Req = requests.post(url, headers = header, data = payload)
		Res = Req.json()
	elif stri == 'get_user_voucher_used':
		token = request.META.get('HTTP_AUTHORIZATION')
		user = Register.objects.get(token = token)
		url = 'https://api.sipromo.id/get/user_voucher/used'
		header = {'Content-Type':'application/json'}
		payload = {
		'appToken': '$2y$10$KMWlIAhy6p8gGPJx7tdgKOOgAIksjaaB6ZLUXWYtKxJH.9m/9oTy6',
		'appID': '92771509',
		'user_id': user.id
		}
		Req = requests.post(url, headers = header, data = payload)
		Res = Req.json()
	elif stri == 'get_user_voucher_expired':
		token = request.META.get('HTTP_AUTHORIZATION')
		user = Register.objects.get(token = token)
		url = 'https://api.sipromo.id/get/user_voucher/used'
		header = {'Content-Type':'application/json'}
		payload = {
		'appToken': '$2y$10$KMWlIAhy6p8gGPJx7tdgKOOgAIksjaaB6ZLUXWYtKxJH.9m/9oTy6',
		'appID': '92771509',
		'user_id': user.id
		}
		Req = requests.post(url, headers = header, data = payload)
		Res = Req.json()
	return Response(Res)