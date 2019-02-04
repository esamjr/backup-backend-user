# from django.shortcuts import render
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from django.views.decorators.csrf import csrf_exempt
# from .models import Attempt
# from registrations.models import Register
# from .serializer import AttemptSerializer
# from datetime import date

# @api_view(['GET'])
# def count_your_blessing(request,):
# 	if request.method == 'GET':
# 		try:
# 			token = Register.objects.get(email = email).id
# 			attempting = Attempt.objects.get(id_user = token).attempt					
# 			if (attempting == 2):
# 				payload = {'date': date.today()}
# 				response = {'status':'ganti hari'}
# 				return Response(response, status=status.HTTP_201_CREATED)
# 			else:
# 				payload = ('attempt' : attempting + 1)	
# 				serializer = GetAttemptSerializer(attempting, data = payload)
# 				if serializer.is_valid():
# 					serializer.save()
# 					return Response(serializer.data, status=status.HTTP_201_CREATED)
# 				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# 		except Attempt.DoesNotExist:
# 			token = Register.objects.get(email = email).id
# 			payload = ('id_user':token, 'attempt' : attempting + 1, 'date': date.today())
# 			serializer = AttemptSerializer(data = payload)
# 			if serializer.is_valid():
# 				serializer.save()
# 				response = {'status':'added new sins'}
# 				return Response(response, status=status.HTTP_201_CREATED)
