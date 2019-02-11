from django.shortcuts import render
from PIL import Image
from pytesseract import image_to_string
from urllib.request import urlopen
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
@csrf_exempt
def OCRT(request, nomor, url):
	if request.method == 'POST':
		link = urlopen(url)
		im = Image.open(link)
		text = image_to_string(im, lang = 'ind')
		if (nomor in text) :
			response = {'status' : 'OK'}
			return Response(response, status = status.HTTP_201_CREATED)
		response = {'status' : 'NOT OK'}
		return Response(response, status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def OCRTx(request):
	url = request.data['url']
	nomor  = request.data['nomor']
	link = urlopen(url)
	im = Image.open(link)
	text = image_to_string(im, lang = 'ind')
	if (nomor in text) :
		return Response({text})
	return Response({text})