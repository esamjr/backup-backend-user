from django.shortcuts import render
from PIL import Image
from pytesseract import image_to_string
from urllib.request import urlopen
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def OCRT(request):
	nama = request.data['nama']
	urlnpwp = request.data['npwp']
	link = urlopen(urlnpwp)
	im = Image.open(link)
	text = image_to_string(im, lang = 'ind')
	if (nama in text) :
		return Response(nama)
	return Response('tidak valid')