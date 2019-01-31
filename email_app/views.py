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
        # recipient = "mail"
        # htmly = get_template('emailtemplate.html')
        # d = ({'username': "maulidan.ksl@gmail.com",'token': 'http://dev-user.mindzzle.com/register/confirmation?token=', 'konten':'To complete your sign up, please verify your email', 'tombol':'Verify Email'})
        # html_content = htmly.render(d)
        requests.post(
            "https://api.mailgun.net/v3/mindzzle.com/messages",
            auth=("api", "868cffd229060b45e4742e6bdd0fdf8c-c8c889c9-ed56b2bf"),
            data={"from": "admin@mindzzle.com",
                  "to": ["maulidan.ksl@gmail.com"],
                  "subject": "percobaan test",
                  "text": "Testing some Mailgun awesomness!",
                  "html" : "<!DOCTYPE html><html xmlns='http://www.w3.org/1999/xhtml' xml:lang='en' lang='en'><head><title>Mindzzle</title><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><meta http-equiv='X-UA-Compatible' content='IE=edge'><style type='text/css'>a,body,table,td{-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%}table,td{mso-table-lspace:0;mso-table-rspace:0}img{-ms-interpolation-mode:bicubic}img{border:0;height:auto;line-height:100%;outline:0;text-decoration:none}table{border-collapse:collapse!important}body{height:100%!important;margin:0!important;padding:0!important;width:100%!important;background-color:#f9f9f9}a[x-apple-data-detectors]{color:inherit!important;text-decoration:none!important;font-size:inherit!important;font-family:inherit!important;font-weight:inherit!important;line-height:inherit!important}@media screen and (max-width:525px){.wrapper{width:100%!important;max-width:100%!important}.logo img{margin:0 auto!important}.mobile-hide{display:none!important}.img-max{max-width:100%!important;width:100%!important;height:auto!important}.responsive-table{width:100%!important}.padding{padding:10px 5% 15px 5%!important}.padding-meta{padding:30px 5% 0 5%!important;text-align:center}.padding-copy{padding:10px 5% 10px 5%!important;text-align:center}.no-padding{padding:0!important}.section-padding{padding:50px 15px 50px 15px!important}}div[style*='margin: 16px 0;']{margin:0!important}</style></head><body style='margin:0!important;padding:0!important'><div style='max-width:600px;margin:0 auto' class='responsive-table'><table border='0' cellpadding='0' cellspacing='0' width='100%'><tr><td align='center'><!--[if (gte mso 9)|(IE)]><table align='center' border='0' cellspacing='0' cellpadding='0' width='500'><tr><td align='center' valign='top' width='500'><![endif]--><table border='0' cellpadding='0' cellspacing='0' width='100%' style='max-width:500px' class='wrapper'><tr><td align='center' valign='top' style='padding:15px 0' class='logo'><a href='http://mindzzle.com' target='_blank'><img alt='Logo' src='https://ucf0797b1b595df4dc4b049bba72.previews.dropboxusercontent.com/p/thumb/AAXJc1VC3LdFsSSAaayh1HjaDHp09jtL07HxqZEDV3dgqA2ZSiE-9ScJp4ZN2weqKefSKHP99jzKa9hF4Ti9NFd1YgNL9hN0oThaInQN-Ppky5CZSYBXELq4LJE5lA9uyMMm6iKGhU38iTdIYhnWk6barRZ10V1_mpOlMmUos5VdoqWBY0aIE-rFuX34FbqTY-mrNr_IZDcP605TeXXnzUnVH6UQ25P_XpX5YXKptcAvLlwaCCscu0Ig0zVTMn1Zn_6Zrjr2UwapRW-uEd0YKyt2/p.png?size_mode=5' style='display:block' border='0'></a></td></tr></table><!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]--></td></tr><tr><td bgcolor='#ffffff' align='center' style='padding:45px 15px 45px 15px;border-top:5px solid #f88203' class='section-padding'><!--[if (gte mso 9)|(IE)]><table align='center' border='0' cellspacing='0' cellpadding='0' width='500'><tr><td align='center' valign='top' width='500'><![endif]--><table border='0' cellpadding='0' cellspacing='0' width='100%' style='max-width:500px' class='responsive-table'><tr><td><table width='100%' border='0' cellspacing='0' cellpadding='0'><tr><td><table width='100%' border='0' cellspacing='0' cellpadding='0'><tr><td align='left' style='font-size:25px;font-family:Helvetica,Arial,sans-serif;font-weight:600;color:#333;padding-top:30px' class='padding'>Hi {{username}},</td></tr><tr><td align='left' style='padding:20px 0 0 0;font-size:16px;line-height:25px;font-family:Helvetica,Arial,sans-serif;color:#343a40' class='padding'>{{konten}}</td></tr></table></td></tr><tr><td align='center'><table width='100%' border='0' cellspacing='0' cellpadding='0'><tr><td align='center' style='padding:35px 0 25px 0' class='padding'><table border='0' cellspacing='0' cellpadding='0'><tr><td align='center' style='border-radius:50px' bgcolor='#243138'><a href='{{token}}' target='_blank' style='font-size:16px;font-family:Helvetica,Arial,sans-serif;color:#fff;text-decoration:none;color:#fff;text-decoration:none;border-radius:50px;padding:15px 45px;display:inline-block' class='mobile-button'><strong>{{tombol}}</strong></a></td></tr></table></td></tr></table></td></tr><tr><td><table width='100%' border='0' cellspacing='0' cellpadding='0'><tr><td align='left' style='padding:20px 0 0 0;font-size:16px;line-height:25px;font-family:Helvetica,Arial,sans-serif;color:#343a40' class='padding'><p>or copy this link and paste it to your web browser</p><p><a href='{{token}}'>{{token}}</a></p><p>&nbsp;</p><p><strong>Cheers,<br>The Mindzzle Team</strong></p></td></tr></table></td></tr></table></td></tr></table><!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]--></td></tr><tr><td align='center' style='padding:20px 0'><!--[if (gte mso 9)|(IE)]><table align='center' border='0' cellspacing='0' cellpadding='0' width='500'><tr><td align='center' valign='top' width='500'><![endif]--><table width='100%' border='0' cellspacing='0' cellpadding='0' align='center' style='max-width:500px' class='responsive-table'><tr><td align='center' style='font-size:12px;line-height:18px;font-family:Helvetica,Arial,sans-serif;color:#666'>Copyright 2018 (c) Mindzzle | Contact | Terms</td></tr></table><!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]--></td></tr></table></div></body></html>"
                 })
        # x = email_log(request, "respondentEmail","sender","subjects")
        response = {'status': 'status Email Sent'}
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