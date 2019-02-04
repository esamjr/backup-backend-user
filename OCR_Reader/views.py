from django.shortcuts import render
from PIL import Image
from pytesseract import image_to_string
from urllib.request import urlopen
from rest_framework.decorators import api_view
from rest_framework.response import Response
# import tesserocr

@api_view(['GET'])
def OCRT(request):
	link = urlopen('https://4.bp.blogspot.com/-UHBY49jyQ3M/WMzeuFOZZxI/AAAAAAAAAUs/Gsv9qPEvM7k3Yz1-z28MKPi1qa4YKqXBgCLcB/s1600/NPWP%2BASAL.jpg')
	im = Image.open(link)
	text = image_to_string(im, lang = 'ind')

	return Response(text)

# print(text)
