from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import User_img
from OCR_Reader.serializers import UserImgSerializer
from registrations.models import Register
from .serializers import ValidSerializer,ExpTaxnumSerializer
from PIL import Image
from pytesseract import image_to_string
from urllib.request import urlopen

@api_view(['GET'])
def get_all_doc(request):
	token = request.META.get('HTTP_AUTHORIZATION')	
	user = Register.objects.get(id = '0')
	if token == user.token:
		datas = User_img.objects.all()
		serializer = UserImgSerializer(datas, many = True)
		return Response(serializer.data, status = status.HTTP_200_OK)

@api_view(['GET'])
def get_doc(request):
	token = request.META.get('HTTP_AUTHORIZATION')
	try:
		user = Register.objects.get(token = token)
		datas = User_img.objects.get(id_user = user.id)
		serializer = UserImgSerializer(datas)
		return Response(serializer.data, status = status.HTTP_200_OK)
	except Register.DoesNotExist:
		return Response({'status':'YOU DID NOT HAVE ACCESS'}, status = status.HTTP_401_UNAUTHORIZED)
	except User_img.DoesNotExist:
		return Response({'status':'YOUR DATA IS NOT AVAILABLE'}, status = status.HTTP_400_BAD_REQUEST)


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
			
		elif (type_name == "npwp"):
			beacon = User_img.objects.get(id_user = token)
			payload = {
				'id_user' : token,
				'type_name' : type_name,
				'no_npwp' : nomor,
				'url_npwp' : url,
				'no_ktp' : beacon.no_ktp,
				'url_ktp' : beacon.url_ktp
				}
			link = urlopen(url)
			im = Image.open(link)
			text = image_to_string(im, lang = 'ind')
			if (nomor in text):
				serializers = UserImgSerializer(beacon, data = payload)
				if serializers.is_valid():			
					serializers.save()
					payloads = {'tax_num': nomor}
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


