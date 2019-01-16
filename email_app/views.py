from django.shortcuts import render
from django.core.mail import send_mail
from registrations.models import Register
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import EmailSerializer
from .models import Email

@api_view(['GET'])
def get_log_email(request):
    network = Email.objects.all()
    serializer = EmailSerializer(network, many=True)
    return Response(serializer.data)

# @api_view(['POST'])
def send_email(mail):
	
	respondentEmail = Register.objects.get(email=mail)

	send_mail(
		'Account Activation',
		'Hi '+respondentEmail.full_name +'Thanks so much for joining Mindzzle! \n To finish signing up, you just need to confirm that we got your email right. Click <a href = "www.google.com">Here</a>',
		'admin@mindzzle.com',
		[respondentEmail.email,'powerrangers@mailinator.com'], 
		fail_silently=False
		)

	payload = {
	'recipient': respondentEmail,
	'sender': 'admin@mindzzle.com',
	'subject':'Account Activation'
	}
	serializer = EmailSerializer(data = payload)
	if serializer.is_valid():
		serializer.save()
	response = {'status':'Email Sent'}
	return Response(response)