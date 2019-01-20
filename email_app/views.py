from django.shortcuts import render
from django.core.mail import send_mail
from registrations.models import Register
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import EmailSerializer
from .models import Email
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
# @api_view(['POST'])
def send_email(request,mail,token, subjects):
# def send_email(request):
	respondentEmail = Register.objects.get(email=mail)
	sender = 'admin@mindzzle.com'
	# subjects = 'Account Activation'
	# respondentEmail = request.data['respondentEmail']
	# sender = request.data['sender']
	# subjects = request.data['subjects']
	# token = 'okasokdianfammcdajsnckm'
	try:		
		send_mail(
			subjects,
			'Hi '+respondentEmail.full_name +'\n Thanks so much for joining Mindzzle! \n To finish signing up, you just need to confirm that we got your email right.\n <a href="http://dev-user.mindzzle.com/register/confirmation?token='+token+'"> Click Here! </a> To verify',
			sender,
			[respondentEmail], 
			fail_silently=False
			)
		email_log(request, respondentEmail,sender,subjects)
		response = {'status Email Sent'}
		return HttpResponse(response)
	except:
		response = {'status failed to send email'}
		return HttpResponse(response)

@csrf_exempt
def email_log(request,respondentEmail,sender,subjects):
	if request.method == 'POST':
		payload = {
		'recipient' : respondentEmail,
		'sender' : sender,
		'subject' : subjects
		}
		serializer = EmailSerializer(data = payload)
		if serializer.is_valid():
			serializer.save()
			content = {'status saved':'saved'}	
			return HttpResponse(content)		
		else:
			content = {'status not saved':'not saved'}
			return HttpResponse(content)


@api_view(['GET'])
def email_get(request):
	if request.method == 'GET':
		network = Email.objects.all()
		serializer = EmailSerializer(network, many=True)
		return Response(serializer.data)



# "http://www.user.mindzzle.com/registrations/api/confirm/'+token+'"