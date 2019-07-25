from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from registrations.models import Register
from django.conf import settings
import requests
import json
# Create your views here.

@api_view(['POST'])
def sipromo(request, stri):
	try:
		if stri =='getvouchers':
			if settings.FLAG == 1 :
				url = 'https://api.sipromo.id/get/vouchers'
			else:
				url = 'http://52.221.178.188/get/vouchers'
			header = {'Content-Type':'application/json'}
			payload = "{\n\t\"appToken\": \"$2y$10$KMWlIAhy6p8gGPJx7tdgKOOgAIksjaaB6ZLUXWYtKxJH.9m/9oTy6\",\n\t\"appID\": \"92771509\"\n}"
			Req = requests.post(url, headers= header, data = payload)
			Res = Req.json()
		elif stri == 'getvoucherdetail':
			if settings.FLAG == 1 :
				url = 'https://api.sipromo.id/get/voucher_detail'
			else:
				url = 'http://52.221.178.188/get/voucher_detail'
			header = {'Content-Type':'application/json'}
			payload = "{\n\t\"appToken\": \"$2y$10$KMWlIAhy6p8gGPJx7tdgKOOgAIksjaaB6ZLUXWYtKxJH.9m/9oTy6\",\n\t\"appID\": \"92771509\",\n\t\"voucher_id\": \""+request.data['voucher_id']+"\"\n}"
			Req = requests.post(url, headers = header, data = payload)
			Res = Req.json()
		elif stri == 'redeemvoucher':
			token = request.META.get('HTTP_AUTHORIZATION')
			user = Register.objects.get(token = token)
			if settings.FLAG == 1 :
				url = 'https://api.sipromo.id/redeem'
			else:
				url = 'http://52.221.178.188/redeem'
			header = {'Content-Type':'application/json'}
			payload = "{\n\t\"appToken\": \"$2y$10$KMWlIAhy6p8gGPJx7tdgKOOgAIksjaaB6ZLUXWYtKxJH.9m/9oTy6\",\n\t\"appID\": \"92771509\",\n\t\"voucher_id\": \""+request.data['voucher_id']+"\",\n\t\"user_id\": \""+user.id+"\"\n}"
			Req = requests.post(url, headers = header, data = payload)
			Res = Req.json()
		elif stri == 'getuservoucherredeem':
			token = request.META.get('HTTP_AUTHORIZATION')
			user = Register.objects.get(token = token)
			if settings.FLAG == 1 :
				url = 'https://api.sipromo.id/get/user_voucher/redeem'
			else:
				url = 'http://52.221.178.188/get/user_voucher/redeem'
			header = {'Content-Type':'application/json'}
			payload = "{\n\t\"appToken\": \"$2y$10$KMWlIAhy6p8gGPJx7tdgKOOgAIksjaaB6ZLUXWYtKxJH.9m/9oTy6\",\n\t\"appID\": \"92771509\",\n\t\"user_id\": \""+user.id+"\"\n}"
			Req = requests.post(url, headers = header, data = payload)
			Res = Req.json()
		elif stri == 'getuservoucherused':
			token = request.META.get('HTTP_AUTHORIZATION')
			user = Register.objects.get(token = token)
			if settings.FLAG == 1 :
				url = 'https://api.sipromo.id/get/user_voucher/used'
			else:
				url = 'http://52.221.178.188/get/user_voucher/used'
			header = {'Content-Type':'application/json'}
			payload = "{\n\t\"appToken\": \"$2y$10$KMWlIAhy6p8gGPJx7tdgKOOgAIksjaaB6ZLUXWYtKxJH.9m/9oTy6\",\n\t\"appID\": \"92771509\",\n\t\"user_id\": \""+user.id+"\"\n}"
			Req = requests.post(url, headers = header, data = payload)
			Res = Req.json()
		elif stri == 'getuservoucherexpired':
			token = request.META.get('HTTP_AUTHORIZATION')
			user = Register.objects.get(token = token)
			if settings.FLAG == 1 :
				url = 'https://api.sipromo.id/get/user_voucher/used'
			else:
				url = 'http://52.221.178.188/get/user_voucher/used'
			header = {'Content-Type':'application/json'}
			payload = "{\n\t\"appToken\": \"$2y$10$KMWlIAhy6p8gGPJx7tdgKOOgAIksjaaB6ZLUXWYtKxJH.9m/9oTy6\",\n\t\"appID\": \"92771509\",\n\t\"user_id\": \""+user.id+"\"\n}"
			Req = requests.post(url, headers = header, data = payload)
			Res = Req.json()
		else:
			return Response({'status':'Endpoint has no match'}, status = status.HTTP_400_BAD_REQUEST)
		return Response([Res])
	except Register.DoesNotExist:
		return Response({'status':'User Did Not Exist'}, status = status.HTTP_401_UNAUTHORIZED) 