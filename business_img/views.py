from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Company_img
from OCR_Reader.serializers import CompImgSerializer
from OCR_Reader.views import OCRT

@api_view(['POST'])
def upload_doc(request):	
	id_company = request.data['id_company']
	type_name = request.data['type_name']
	url = request.data['url']
	nomor = request.data['nomor']
	status = request.data['status']
	payload = {
		'id_company':id_company,
		'type_name':type_name,
		'url':url,
		'nomor':nomor,
		'status':status
	}	
	serializers = CompImgSerializer(data = payload)
	if serializers.is_valid():
		OCRT(request, nomor, url)
		serializer.save()
		return Response(OCRT, status = status.HTTP_201_CREATED)
	return Response(OCRT, status = status.HTTP_400_BAD_REQUEST)