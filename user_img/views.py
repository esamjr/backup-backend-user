from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import User_img
from OCR_Reader.serializers import UserImgSerializer
from registrations.models import Register
from .serializers import ValidSerializer,ExpTaxnumSerializers
from PIL import Image
from pytesseract import image_to_string
from urllib.request import urlopen

@api_view(['POST'])
def upload_doc(request):
	try:
		get_token = request.META.get('HTTP_AUTHORIZATION')
		token = Register.objects.get(token = get_token).id
		user = Register.objects.get(token = get_token)
		type_name = request.data['type_name']
		url = request.data['url']
		nomor = request.data['nomor']
		
		if (type_name == "ktp"):
			payload = {
				'id_user' : token,
				'type_name' : type_name,
				'no_ktp' : nomor,
				'url_ktp' : url,
				'status' : "1"}
			# link = urlopen(url)
			# im = Image.open(link)
			# text = image_to_string(im, lang = 'ind')			
			# if (nomor in url):
			serializers = UserImgSerializer(data = payload)
			if serializers.is_valid():			
				serializers.save()
				payloads = {'ssn_num':nomor,
							'verfied':"1"}
				serializer2 = ValidSerializer(user, data = payloads)
				if serializer2.is_valid():
					serializer2.save()
					response = {'status' : 'OK'}
					return Response(response, status = status.HTTP_201_CREATED)
				return Response(serializer2.errors, status = status.HTTP_400_BAD_REQUEST)
			return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)
			# else:
			# 	response = {'status' : 'KTP TIDAK VALID'}
			# 	return Response(response, status = status.HTTP_400_BAD_REQUEST)

		elif (type_name == "npwp"):
			beacon = User_img.objects.get(id_user = token)
			payload = {
				'id_user' : token,
				'type_name' : type_name,
				'no_npwp' : nomor,
				'url_npwp' : url,
				'no_ktp' : beacon.no_ktp,
				'url_ktp' : beacon.url_ktp,
				}
			link = urlopen(url)
			im = Image.open(link)
			text = image_to_string(im, lang = 'ind')
			if (nomor in text):
				serializers = UserImgSerializer(beacon, data = payload)
				if serializers.is_valid():			
					serializers.save()
					payloads = ('tax_num':nomor)
					serializer2 = ExpTaxnumSerializer(user, data = payloads)
					if serializer2.is_valid():
						serializer2.save()
						response = {'status' : 'OK'}
						return Response(response, status = status.HTTP_201_CREATED)
					return Response(serializer2.errors, status = status.HTTP_400_BAD_REQUEST)
				return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)
			else:
				response = {'status' : 'NPWP TIDAK VALID'}
				return Response(response, status = status.HTTP_400_BAD_REQUEST)
	except Register.DoesNotExist:
		response = {'status' : 'Register Does Not Exist'}
		return Response(response, status = status.HTTP_401_UNAUTHORIZED)


	# try :
	# 	get_token = request.META.get('HTTP_AUTHORIZATION')
	# 	token = Register.objects.get(token = get_token).id
	# 	type_name = request.data['type_name']
	# 	url = request.data['url']
	# 	nomor = request.data['nomor']
	# 	no_ktp = request.data['no_ktp']
	# 	url_ktp = request.data['url_ktp']
	# 	# status = request.data['status']
	# 	payload = {
	# 			'id_user' : token,
	# 			'type_name' : type_name,
	# 			'url' : url,
	# 			'nomor' : nomor,
	# 			'ktp' : no_ktp,
	# 			'url_ktp' : url_ktp,
	# 			'status' : "1"}

	# 	link = urlopen(url)
	# 	link_ktp = urlopen(url_ktp)
	# 	im_ktp = Image.open(link_ktp)
	# 	im = Image.open(link)
	# 	text_ktp = image_to_string(im_ktp, lang = 'ind')
	# 	text = image_to_string(im, lang = 'ind')
	# 	if (no_ktp in text_ktp):
	# 		if (nomor in text) :
	# 			serializers = UserImgSerializer(data = payload)
	# 			if serializers.is_valid():			
	# 				serializers.save()
	# 				response = {'status' : 'OK'}
	# 				return Response(response, status = status.HTTP_201_CREATED)
	# 			return Response(serializers.errors, status = status.HTTP_201_CREATED)
	# 		else:			
	# 			response = {'status' : 'NPWP TIDAK VALID'}
	# 			return Response(response, status = status.HTTP_400_BAD_REQUEST)
	# 	else:			
	# 		response = {'status' : 'KTP TIDAK VALID'}
	# 		return Response(response, status = status.HTTP_400_BAD_REQUEST)

	# except Register.DoesNotExist:
	# 	response = {'status' : 'Register Does Not Exist'}
	# 	return Response(response, status = status.HTTP_401_UNAUTHORIZED)