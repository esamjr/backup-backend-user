from django.shortcuts import render
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from registrations.models import Register
from .models import Notification
from .serializers import NotificationSerializer
from pyfcm import FCMNotification
import time

@csrf_exempt
def notification_user(request, modelUser, messages):
	users = modelUser
	userid = users.id
	message =  messages
	state = 1
	payload = {
	'id_user' : userid,
	'messages' : message,
	'status' : state
	}
	serializers = NotificationSerializer(data=payload)
	if serializers.is_valid():
		serializers.save()
		response = {'status':'successfull'}
		return Response(response, status = status.HTTP_201_CREATED)
	return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)
	
@api_view(['POST', 'GET'])
def notifications_fcm(request):
	if request.method == 'POST':
		push_service = FCMNotification(api_key="BFOZH3SLT4LlgDpBwZ75AuX6KecwnkC7rLbhFxCULWnUqLQfLcZxO5Fizf7nMuazV_E9kc4eFMIBgl20aVhuyCI")
		registration_id = request.body['device_id']
		message_title = "Uber update"
		message_body = "Hi john, your customized news for today is ready"
		# result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
		push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
		response = {'status':'successfull'}
		return Response(response, status = status.HTTP_201_CREATED)

	elif request.method == 'GET':
		network = Notification.objects.all()
		serializer = NotificationSerializer(network, many=True)
		return Response(serializer.data)

	return Response({'ERROR':'THIS IS ERROR MESSAGE'}, status = status.HTTP_400_BAD_REQUEST)


	# # Send to multiple devices by passing a list of ids.
	# registration_ids = ["<device registration_id 1>", "<device registration_id 2>", ...]
	# message_title = "Uber update"
	# message_body = "Hope you're having fun this weekend, don't forget to check today's news"
	# result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)

	# print result
