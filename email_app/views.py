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
def send_email(mail,token):
	
	respondentEmail = Register.objects.get(email=mail)

	send_mail(
		'Account Activation',
		'Hi '+respondentEmail.full_name +'\n Thanks so much for joining Mindzzle! \n To finish signing up, you just need to confirm that we got your email right.\n click this button to verify your account \n <button href ="http://127.0.0.1:8000/registrations/api/confirm/"'+token+'">Verify Account</button> \n <a href="http://127.0.0.1:8000/registrations/api/confirm/'+token+'"> Click Here! </a> To verify',
		'admin@mindzzle.com',
		[respondentEmail.email], 
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


	# "http://www.user.mindzzle.com/registrations/api/confirm/'+token+'"