from django.shortcuts import render
from django.core.mail import send_mail
from registrations.models import Register
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import EmailSerializer
from .models import Email
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template import loader
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from django.conf.urls import include
import requests


@csrf_exempt
def send_forget_email(request,mail,token, name, subjects):
    respondentEmail = mail
    sender = 'admin@mindzzle.com'	
    try:		
        htmly = get_template('emailtemplate.html')
        d = ({'username': name,'token': 'http://dev-user.mindzzle.com/register/confirmation?token='+token, 'konten':'To reset your password, please click the button below', 'tombol':'Forget Password'})
        html_content = htmly.render(d)
        requests.post(
            "https://api.mailgun.net/v3/mindzzle.com/messages",
            auth=("api", "868cffd229060b45e4742e6bdd0fdf8c-c8c889c9-ed56b2bf"),
            data={"from": "admin@mindzzle.com",
                  "to": ["maulidan.ksl@gmail.com"],
                  "subject": subjects,
                  "text": "Testing some Mailgun awesomness!",
                  "html": html_content})
        x = email_log(request, respondentEmail,sender,subjects)
        response = {'status': 'Email Sent forget', 'log':x}
        return HttpResponse(response)
    except:
        response = {'status failed to send email'}
        return HttpResponse(response)

@api_view(['GET'])
def send_email(request):
    respondentEmail = "mail"
    sender = 'admin@mindzzle.com'	
    try:		
        recipient = "mail"
        htmly = get_template('emailtemplate.html')
        d = ({'username': "maulida.ksl@gmail.com",'token': 'http://dev-user.mindzzle.com/register/confirmation?token=', 'konten':'To complete your sign up, please verify your email', 'tombol':'Verify Email'})
        html_content = htmly.render(d)
        requests.post(
            "https://api.mailgun.net/v3/mindzzle.com/messages",
            auth=("api", "868cffd229060b45e4742e6bdd0fdf8c-c8c889c9-ed56b2bf"),
            data={"from": "admin@mindzzle.com",
                  "to": ["maulidan.ksl@gmail.com"],
                  "subject": "subjects",
                  "text": "Testing some Mailgun awesomness!",
                  "html": html_content})
        x = email_log(request, "respondentEmail","sender","subjects")
        response = {'status': 'status Email Sent', 'log':x}
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