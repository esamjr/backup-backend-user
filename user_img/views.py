from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import User_img
from OCR_Reader.serializers import UserImgSerializer
from registrations.models import Register
@api_view(['POST'])
def upload_doc(request):
	try :
		tokenx = request.META.get('HTTP_AUTHORIZATION')
		token = Register.objects.get(token = tokenx)
		payload = {
				'id_user' : token,
				'type_name' : request.data['type'],
				'url' : request.data['url'],
				'nomor' : request.data['number'],
				'status' : request.data['status']}
		serializers = UserImgSerializer(data = request.data)
		if serializers.is_valid():
			serializer.save()
			return Response(serializer.data, status = status.HTTP_201_CREATED)
		return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
	except Register.DoesNotExist:
		response = {'status' : 'UNAUTHORIZED'}
		return Response(response, status = status.HTTP_401_UNAUTHORIZED)