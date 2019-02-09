from django.shortcuts import render
from PIL import Image
from pytesseract import image_to_string
from urllib.request import urlopen
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def OCRT(request, nomor, url):	
	link = urlopen(url)
	im = Image.open(link)
	text = image_to_string(im, lang = 'ind')
	if (nomor in text) :
		return Response({nomor})
	return Response({'tidak valid'})

@api_view(['POST'])
def OCRTx(request):
	url = request.data['url']
	nomor  = request.data['nomor']
	link = urlopen(url)
	im = Image.open(link)
	text = image_to_string(im, lang = 'ind')
	if (nomor in text) :
		return Response({nomor})
	return Response({'tidak valid'})