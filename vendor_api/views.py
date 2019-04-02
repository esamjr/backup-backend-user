from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Vendor_api
from rest_framework_jwt.settings import api_settings
from .serializers import VendorSerializer
from django.contrib.auth.hashers import check_password, make_password, is_password_usable
from registrations.models import Register

@api_view(['GET', 'POST'])
def generate(request):
	if request.method == 'POST':
		# jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
		# jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

		vendor = request.data['vendors']
		username = request.data['username']
		password = request.data['password']
		hashes = ''.join(str(ord(c))for c in vendor)

		# payload = jwt_payload_handler(username)
		# token = jwt_encode_handler(payload)
		# token = request.data['token']

		payloads = {
			'username' : username,
			'password' : make_password(str(hashes) + str(password)),
			'vendor_name' : vendor,
			'token' : make_password(str(hashes) + 'Mind55L3')
		}
		serializer = VendorSerializer(data = payloads)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	elif request.method == 'GET':
		try:
			token = request.META.get('HTTP_AUTHORIZATION')
			user = Register.objects.get(token = token)
			if user.id == '0':
				network = Vendor_api.objects.all()
				serializer = VendorSerializer(network, many=True)
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			else:
				return Response({'status':'YOU DONT HAVE ACCESS'}, status = status.HTTP_401_UNAUTHORIZED)
		except Register.DoesNotExist:
			return Response({'status':'YOU DONT HAVE ACCESS.'}, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def login_logout_vendors(request):
	if request.method == 'POST':
		try:
			username = request.data['username']
			password = request.data['password']
			beacon = Vendor_api.objects.get(username = username)
			hashes = ''.join(str(ord(c))for c in beacon.vendor_name)
			key = hashes + password
			if (check_password(key , beacon.password)):
				payloads = {
					'username' : username,
					'password' : make_password(str(hashes) + str(password)),
					'vendor_name' : beacon.vendor_name,
					'token' : make_password(str(hashes) + 'Mind55L3')
				}
				serializer = VendorSerializer(beacon,data = payloads)
				if serializer.is_valid():
					serializer.save()
					return Response( serializer.data, status = status.HTTP_202_ACCEPTED)
				return Response( serializer.errors, status = status.HTTP_400_BAD_REQUEST)
			else:
				return Response({'status':'wrong username / password'}, status = status.HTTP_401_UNAUTHORIZED)
		except Vendor_api.DoesNotExist:
			return Response({'status':'YOU DONT HAVE ACCESS.'}, status = status.HTTP_400_BAD_REQUEST)
	elif request.method == 'GET':
		try:
			token = request.META.get('HTTP_AUTHORIZATION')
			beacon = Vendor_api.objects.get(token = token)
			payload = {
				'username': beacon.username,
				'password': beacon.password,
				'vendor_name': beacon.vendor_name,
				'token': 'xxx'
				}
			serializer = VendorSerializer(beacon, data = payload)
			if serializer.is_valid():
				serializer.save()
				return Response({'status':'YOU HAS LOGOUT'}, status = status.HTTP_202_ACCEPTED)
			return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
		except Vendor_api.DoesNotExist:
			return Response({'status':'YOU MOST LOGIN FIRST.'}, status = status.HTTP_401_UNAUTHORIZED)
