from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import User_img
from OCR_Reader.serializers import UserImgSerializer
from registrations.models import Register
from OCR_Reader.views import OCRT
@api_view(['POST'])
def upload_doc(request):
	try :
		get_token = request.META.get('HTTP_AUTHORIZATION')
		token = Register.objects.get(token = get_token).id
		type_name = request.data['type_name']
		url = request.data['url']
		nomor = request.data['nomor']
		# status = request.data['status']
		payload = {
				'id_user' : token,
				'type_name' : type_name,
				'url' : url,
				'nomor' : nomor,
				'status' : "1"}
		OCRT(request, nomor, url)
		serializers = UserImgSerializer(data = payload)
		if serializers.is_valid():			
			serializers.save()
			response = {'status' : 'OK'}
			return Response(response, status = status.HTTP_201_CREATED)
		response = {'status' : 'NOT OK'}
		return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)
	except Register.DoesNotExist:
		response = {'status' : 'Register Does Not Exist'}
		return Response(response, status = status.HTTP_401_UNAUTHORIZED)