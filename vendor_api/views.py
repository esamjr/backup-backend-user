from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Vendor_api
from rest_framework_jwt.settings import api_settings
from .serializers import VendorSerializer

@api_view(['GET', 'POST'])
def generate(request):
	if request.method == 'POST':
		jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
		jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

		vendor = request.data['vendors']
		username = request.data['username']
		password = request.data['password']
		payload = jwt_payload_handler(username)
		token = jwt_encode_handler(payload)
		# token = request.data['token']

		payloads = {
		'username' : username,
		'password' : password,
		'vendor_name' : vendor,
		'token' : token
		}
		serializer = VendorSerializer(data = payloads)
		if serializer.is_valid():
			serializer.save
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	elif request.method == 'GET':
		network = Vendor_api.objects.all()
		serializer = VendorSerializer(network, many=True)
		return Response(serializer.data, status=status.HTTP_201_CREATED)

