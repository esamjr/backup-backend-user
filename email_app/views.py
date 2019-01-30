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


@csrf_exempt
def send_forget_email(request,mail,token, name, subjects):
	respondentEmail = mail
	sender = 'admin@mindzzle.com'	
	try:		
		plaintext = get_template('email.txt')
		htmly     = get_template('emailtemplate.html')
		d = ({'username': name,'token': 'http://dev-user.mindzzle.com/register/confirmation?token='+token, 'konten':'To complete your reset password, press the button below','tombol':'Forget Password'})
		subject, from_email, to = subjects, sender, respondentEmail
		text_content = plaintext.render(d)
		html_content = htmly.render(d)
		msg = EmailMultiAlternatives(subjects, text_content, sender, [mail])
		msg.attach_alternative(html_content, "text/html")
		msg.send()
		response = {'status Email Sent'}
		return HttpResponse(response)
	except:
		response = {'status failed to send email'}
		return HttpResponse(response)

# @csrf_exempt
# def send_email(request, mail, token, name, subjects):
# 	respondentEmail = mail
# 	sender = 'admin@mindzzle.com'	
# 	try:		
# 		plaintext = get_template('email.txt')
# 		htmly     = get_template('emailtemplate.html')
# 		d = ({'username': name,'token': 'http://dev-user.mindzzle.com/register/confirmation?token='+token, 'konten':'To complete your sign up, please verify your email', 'tombol':'Verify Email'})
# 		subject, from_email, to = subjects, sender, respondentEmail
# 		text_content = plaintext.render(d)
# 		html_content = htmly.render(d)
# 		msg = EmailMultiAlternatives(subjects, text_content, sender, [mail])
# 		msg.attach_alternative(html_content, "text/html")
# 		msg.send()
# 		email_log(request, respondentEmail,sender,subjects)
# 		response = {'status Email Sent'}
# 		return HttpResponse(response)
# 	except:
# 		response = {'status failed to send email'}
# 		return HttpResponse(response)


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


# @csrf_exempt
@api_view(['POST'])
# def send_email(request,mail,token, subjects):
def send_email(request):
	# respondentEmail = mail

	sender = 'admin@mindzzle.com'
	subjects = 'Account Activation'
	respondentEmail = request.data['respondentEmail']
	name = request.data['sender']
	# subjects = request.data['subjects']
	token = 'okasokdianfammcdajsnckm'
	try:		
	
		plaintext = get_template('email.txt')
		htmly     = get_template('emailtemplate.html')

		d = ({'username': name,'token': 'http://dev-user.mindzzle.com/register/confirmation?token='+token, 'konten':'To complete your sign up, please verify your email', 'tombol':'Verify Email'})

		subject, from_email, to = subjects, sender, respondentEmail
		text_content = plaintext.render(d)
		html_content = htmly.render(d)
		msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
		msg.attach_alternative(html_content, "text/html")
		msg.send()
		response = {'success to send email'}
		return HttpResponse(response)
	except:
		response = {'status failed to send email'}
		return HttpResponse(response)


# "http://www.user.mindzzle.com/registrations/api/confirm/'+token+'"