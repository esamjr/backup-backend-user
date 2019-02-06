from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Company_img
from OCR_Reader.serializers import CompImgSerializer


@api_view(['POST'])
def upload_doc(request):	
	serializers = CompImgSerializer(data = request.data)
	if serializers.is_valid():
		serializer.save()
		return Response(serializer.data, status = status.HTTP_201_CREATED)
	return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)