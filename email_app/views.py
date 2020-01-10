import datetime
import requests
import re


from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

from partner_api.utils import render_to_string_with_context
from registrations.models import Register
from .models import Email
from .serializers import EmailSerializer

SERVER_PROD = settings.SITE_URL
sender = 'admin@mindzzle.com'


def send_emails(subject, to_email, message_html, message_text=None, from_email=settings.DEFAULT_FROM_EMAIL):
    if not message_text:
        message_text = message_html
    email = EmailMultiAlternatives(
        subject, message_text, to=[to_email], from_email=from_email
    )
    email.attach_alternative(message_html, 'text/html')
    email.send()


def links_url(request):
    link_req = requests.get()
    link_url = re.split(settings.API_URL, link_req)
    return link_url


@csrf_exempt
def email_log(request, respondentEmail, sender, subjects):
    payload = {
        'recipient': respondentEmail,
        'sender': sender,
        'subject': subjects
    }
    serializer = EmailSerializer(data=payload)
    if serializer.is_valid():
        serializer.save()
        content = {'status': 'saved'}
        return HttpResponse(content)
    else:
        content = {'status': 'not saved'}
        return HttpResponse(content)


@csrf_exempt
def forget_pass(request, token):
    if settings.FLAG == 1:
        link = 'https://x-user.mindzzle.com/password/new?token=' + token
        # return link
    elif settings.FLAG == 2:
        link = 'http://staging-user.mindzzle.com/password/new?token=' + token
        # return link
    else:
        link = 'http://localhost:8000/password/new?token=' + token
    return link


@csrf_exempt
def confrlink(request, token):
    if settings.DEBUG:
        link = 'http://dev-user.mindzzle.com/register/confirmation?token=' + token
    elif not settings.DEBUG:
        link = 'http://x-user.mindzzle.com/register/confirmation?token=' + token
    return link


def send_forget_email(request):

    reset_pass = settings.SITE_URL + 'password/new?token=' + request['token']

    data = {
        'from_email': settings.DEFAULT_FROM_EMAIL,
        'recipient_email': request['mail'],
        'name': request['name'],
        'mail_subject': request['subjects'],
        'token': request['token'],
        'link': reset_pass
    }

    message_html = render_to_string_with_context('emails/email_password_reset.html', **data)
    send_emails(request['subjects'], request['mail'], message_html)


@api_view(['POST'])
def resend_email(request):
    respondentEmail = mail
    subjects = 'Activation account'
    mail = requests.data['email']
    beacon = Register.objects.get(email=mail)
    name = beacon.full_name
    token = beacon.token
    try:
        requests.post(
            "http://email-app.mindzzle.com/mailsent/",
            data={"from": "admin@mindzzle.com",
                  "to": mail,
                  "subjects": subjects,
                  "text": "Activation Email!",
                  "html": "<!DOCTYPE html><html xmlns='http://www.w3.org/1999/xhtml' xml:lang='en' lang='en'><head><title>Mindzzle</title><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><meta http-equiv='X-UA-Compatible' content='IE=edge'><style type='text/css'>a,body,table,td{-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%}table,td{mso-table-lspace:0;mso-table-rspace:0}img{-ms-interpolation-mode:bicubic}img{border:0;height:auto;line-height:100%;outline:0;text-decoration:none}table{border-collapse:collapse!important}body{height:100%!important;margin:0!important;padding:0!important;width:100%!important;background-color:rgb(249, 249, 249)}a[x-apple-data-detectors]{color:inherit!important;text-decoration:none!important;font-size:inherit!important;font-family:inherit!important;font-weight:inherit!important;line-height:inherit!important}@media screen and (max-width:525px){.wrapper{width:100%!important;max-width:100%!important}.logo img{margin:0 auto!important}.mobile-hide{display:none!important}.img-max{max-width:100%!important;width:100%!important;height:auto!important}.responsive-table{width:100%!important}.padding{padding:10px 5% 15px 5%!important}.padding-meta{padding:30px 5% 0 5%!important;text-align:center}.padding-copy{padding:10px 5% 10px 5%!important;text-align:center}.no-padding{padding:0!important}.section-padding{padding:50px 15px 50px 15px!important}}div[style*='margin: 16px 0;']{margin:0!important}</style></head><body style='margin:0!important;padding:0!important'><div style='max-width:600px;margin:0 auto' class='responsive-table'><table border='0' cellpadding='0' cellspacing='0' width='100%'><tr><td align='center'><!--[if (gte mso 9)|(IE)]><table align='center' border='0' cellspacing='0' cellpadding='0' width='500'><tr><td align='center' valign='top' width='500'><![endif]--><table border='0' cellpadding='0' cellspacing='0' width='100%' style='max-width:500px' class='wrapper'><tr><td align='center' valign='top' style='padding:15px 0' class='logo'><a href='http://mindzzle.com' target='_blank'><img alt='Logo' src='https://firebasestorage.googleapis.com/v0/b/mindzzle-225411.appspot.com/o/logo_mindzzle%2Ftemplates_mindzzle-logo-smaller.png?alt=media&token=75c0869d-020d-4f75-984f-f29100a173a2' style='display:block' border='0'></a></td></tr></table><!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]--></td></tr><tr><td bgcolor='White' align='center' style='padding:45px 15px 45px 15px;border-top:5px solid rgb(248, 130, 3)' class='section-padding'><!--[if (gte mso 9)|(IE)]><table align='center' border='0' cellspacing='0' cellpadding='0' width='500'><tr><td align='center' valign='top' width='500'><![endif]--><table border='0' cellpadding='0' cellspacing='0' width='100%' style='max-width:500px' class='responsive-table'><tr><td><table width='100%' border='0' cellspacing='0' cellpadding='0'><tr><td><table width='100%' border='0' cellspacing='0' cellpadding='0'><tr><td align='left' style='font-size:25px;font-family:Helvetica,Arial,sans-serif;font-weight:600;color:rgb(51, 51, 51);padding-top:30px' class='padding'>Hi " + name + ",</td></tr><tr><td align='left' style='padding:20px 0 0 0;font-size:16px;line-height:25px;font-family:Helvetica,Arial,sans-serif;color:rgb(52, 58, 64)' class='padding'>To activate your Mindzzle account, please click the button below</td></tr></table></td></tr><tr><td align='center'><table width='100%' border='0' cellspacing='0' cellpadding='0'><tr><td align='center' style='padding:35px 0 25px 0' class='padding'><table border='0' cellspacing='0' cellpadding='0'><tr><td align='center' style='border-radius:50px' bgcolor='rgb(36, 49, 56)'><a href='" + confrlink(
                      request,
                      token) + "' target='_blank' style='font-size:16px;font-family:Helvetica,Arial,sans-serif;color:white;text-decoration:none;color:white;text-decoration:none;border-radius:50px;padding:15px 45px;display:inline-block' class='mobile-button'><strong>Activate Account</strong></a></td></tr></table></td></tr></table></td></tr><tr><td><table width='100%' border='0' cellspacing='0' cellpadding='0'><tr><td align='left' style='padding:20px 0 0 0;font-size:16px;line-height:25px;font-family:Helvetica,Arial,sans-serif;color:rgb(52, 58, 64)' class='padding'><p>or copy this link and paste it to your web browser</p><p><a href='" + confrlink(
                      request, token) + "'>" + confrlink(request,
                                                         token) + "</a></p><p>&nbsp;</p><p><strong>Cheers,<br>The Mindzzle Team</strong></p></td></tr></table></td></tr></table></td></tr></table><!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]--></td></tr><tr><td align='center' style='padding:20px 0'><!--[if (gte mso 9)|(IE)]><table align='center' border='0' cellspacing='0' cellpadding='0' width='500'><tr><td align='center' valign='top' width='500'><![endif]--><table width='100%' border='0' cellspacing='0' cellpadding='0' align='center' style='max-width:500px' class='responsive-table'><tr><td align='center' style='font-size:12px;line-height:18px;font-family:Helvetica,Arial,sans-serif;color:black'>Copyright 2018 (c) Mindzzle | Contact | Terms</td></tr></table><!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]--></td></tr></table></div></body></html>"
                  })
        response = {'status': 'Email Sent'}
        email_log(request, mail, "OK", subjects)
        return HttpResponse(response)
    except:
        response = {'status': 'failed to send email'}
        email_log(request, mail, "NOT OK", subjects)
        return HttpResponse(response)


@csrf_exempt
def send_email(request, mail, token, name, subjects):
    respondentEmail = mail
    sender = 'admin@mindzzle.com'
    try:
        requests.post(
            "http://email-app.mindzzle.com/mailsent/",
            data={"from": "admin@mindzzle.com",
                  "to": mail,
                  "subjects": subjects,
                  "text": "Activation Email!",
                  "html": "<!DOCTYPE html><html xmlns='http://www.w3.org/1999/xhtml' xml:lang='en' lang='en'><head><title>Mindzzle</title><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><meta http-equiv='X-UA-Compatible' content='IE=edge'><style type='text/css'>a,body,table,td{-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%}table,td{mso-table-lspace:0;mso-table-rspace:0}img{-ms-interpolation-mode:bicubic}img{border:0;height:auto;line-height:100%;outline:0;text-decoration:none}table{border-collapse:collapse!important}body{height:100%!important;margin:0!important;padding:0!important;width:100%!important;background-color:rgb(249, 249, 249)}a[x-apple-data-detectors]{color:inherit!important;text-decoration:none!important;font-size:inherit!important;font-family:inherit!important;font-weight:inherit!important;line-height:inherit!important}@media screen and (max-width:525px){.wrapper{width:100%!important;max-width:100%!important}.logo img{margin:0 auto!important}.mobile-hide{display:none!important}.img-max{max-width:100%!important;width:100%!important;height:auto!important}.responsive-table{width:100%!important}.padding{padding:10px 5% 15px 5%!important}.padding-meta{padding:30px 5% 0 5%!important;text-align:center}.padding-copy{padding:10px 5% 10px 5%!important;text-align:center}.no-padding{padding:0!important}.section-padding{padding:50px 15px 50px 15px!important}}div[style*='margin: 16px 0;']{margin:0!important}</style></head><body style='margin:0!important;padding:0!important'><div style='max-width:600px;margin:0 auto' class='responsive-table'><table border='0' cellpadding='0' cellspacing='0' width='100%'><tr><td align='center'><!--[if (gte mso 9)|(IE)]><table align='center' border='0' cellspacing='0' cellpadding='0' width='500'><tr><td align='center' valign='top' width='500'><![endif]--><table border='0' cellpadding='0' cellspacing='0' width='100%' style='max-width:500px' class='wrapper'><tr><td align='center' valign='top' style='padding:15px 0' class='logo'><a href='http://mindzzle.com' target='_blank'><img alt='Logo' src='https://firebasestorage.googleapis.com/v0/b/mindzzle-225411.appspot.com/o/logo_mindzzle%2Ftemplates_mindzzle-logo-smaller.png?alt=media&token=75c0869d-020d-4f75-984f-f29100a173a2' style='display:block' border='0'></a></td></tr></table><!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]--></td></tr><tr><td bgcolor='White' align='center' style='padding:45px 15px 45px 15px;border-top:5px solid rgb(248, 130, 3)' class='section-padding'><!--[if (gte mso 9)|(IE)]><table align='center' border='0' cellspacing='0' cellpadding='0' width='500'><tr><td align='center' valign='top' width='500'><![endif]--><table border='0' cellpadding='0' cellspacing='0' width='100%' style='max-width:500px' class='responsive-table'><tr><td><table width='100%' border='0' cellspacing='0' cellpadding='0'><tr><td><table width='100%' border='0' cellspacing='0' cellpadding='0'><tr><td align='left' style='font-size:25px;font-family:Helvetica,Arial,sans-serif;font-weight:600;color:rgb(51, 51, 51);padding-top:30px' class='padding'>Hi " + name + ",</td></tr><tr><td align='left' style='padding:20px 0 0 0;font-size:16px;line-height:25px;font-family:Helvetica,Arial,sans-serif;color:rgb(52, 58, 64)' class='padding'>To activate your Mindzzle account, please click the button below</td></tr></table></td></tr><tr><td align='center'><table width='100%' border='0' cellspacing='0' cellpadding='0'><tr><td align='center' style='padding:35px 0 25px 0' class='padding'><table border='0' cellspacing='0' cellpadding='0'><tr><td align='center' style='border-radius:50px' bgcolor='rgb(36, 49, 56)'><a href='" + confrlink(
                      request,
                      token) + "' target='_blank' style='font-size:16px;font-family:Helvetica,Arial,sans-serif;color:white;text-decoration:none;color:white;text-decoration:none;border-radius:50px;padding:15px 45px;display:inline-block' class='mobile-button'><strong>Activate Account</strong></a></td></tr></table></td></tr></table></td></tr><tr><td><table width='100%' border='0' cellspacing='0' cellpadding='0'><tr><td align='left' style='padding:20px 0 0 0;font-size:16px;line-height:25px;font-family:Helvetica,Arial,sans-serif;color:rgb(52, 58, 64)' class='padding'><p>or copy this link and paste it to your web browser</p><p><a href='" + confrlink(
                      request, token) + "'>" + confrlink(request,
                                                         token) + "</a></p><p>&nbsp;</p><p><strong>Cheers,<br>The Mindzzle Team</strong></p></td></tr></table></td></tr></table></td></tr></table><!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]--></td></tr><tr><td align='center' style='padding:20px 0'><!--[if (gte mso 9)|(IE)]><table align='center' border='0' cellspacing='0' cellpadding='0' width='500'><tr><td align='center' valign='top' width='500'><![endif]--><table width='100%' border='0' cellspacing='0' cellpadding='0' align='center' style='max-width:500px' class='responsive-table'><tr><td align='center' style='font-size:12px;line-height:18px;font-family:Helvetica,Arial,sans-serif;color:black'>Copyright 2018 (c) Mindzzle | Contact | Terms</td></tr></table><!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]--></td></tr></table></div></body></html>"
                  })
        response = {'status': 'Email Sent'}
        email_log(request, mail, "OK", subjects)
        return HttpResponse(response)
    except:
        response = {'status': 'failed to send email'}
        email_log(request, mail, "NOT OK", subjects)
        return HttpResponse(response)


@csrf_exempt
def intervied_email(request, compname, mail, date, time, place):
    respondentEmail = mail
    subjects = 'Invitation Email'
    sender = 'admin@mindzzle.com'
    try:
        requests.post(
            "http://email-app.mindzzle.com/mailsent/",
            data={"from": "no-reply@mindzzle.com",
                  "to": mail,
                  "subjects": subjects,
                  "text": "Invitation Email!",
                  "html": "<!DOCTYPE html><html xmlns='http://www.w3.org/1999/xhtml' xml:lang='en' lang='en'><head><title>Mindzzle</title><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><meta http-equiv='X-UA-Compatible' content='IE=edge'><style type='text/css'>a,body,table,td{-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%}table,td{mso-table-lspace:0;mso-table-rspace:0}img{-ms-interpolation-mode:bicubic}img{border:0;height:auto;line-height:100%;outline:0;text-decoration:none}table{border-collapse:collapse!important}body{height:100%!important;margin:0!important;padding:0!important;width:100%!important;background-color:rgb(249, 249, 249)}a[x-apple-data-detectors]{color:inherit!important;text-decoration:none!important;font-size:inherit!important;font-family:inherit!important;font-weight:inherit!important;line-height:inherit!important}@media screen and (max-width:525px){.wrapper{width:100%!important;max-width:100%!important}.logo img{margin:0 auto!important}.mobile-hide{display:none!important}.img-max{max-width:100%!important;width:100%!important;height:auto!important}.responsive-table{width:100%!important}.padding{padding:10px 5% 15px 5%!important}.padding-meta{padding:30px 5% 0 5%!important;text-align:center}.padding-copy{padding:10px 5% 10px 5%!important;text-align:center}.no-padding{padding:0!important}.section-padding{padding:50px 15px 50px 15px!important}}div[style*='margin: 16px 0;']{margin:0!important}</style></head><body style='margin:0!important;padding:0!important'><div style='max-width:600px;margin:0 auto' class='responsive-table'><table border='0' cellpadding='0' cellspacing='0' width='100%'><tr><td align='center'><!--[if (gte mso 9)|(IE)]><table align='center' border='0' cellspacing='0' cellpadding='0' width='500'><tr><td align='center' valign='top' width='500'><![endif]--><table border='0' cellpadding='0' cellspacing='0' width='100%' style='max-width:500px' class='wrapper'><tr><td align='center' valign='top' style='padding:15px 0' class='logo'><a href='http://mindzzle.com' target='_blank'><img alt='Logo' src='https://firebasestorage.googleapis.com/v0/b/mindzzle-225411.appspot.com/o/logo_mindzzle%2Ftemplates_mindzzle-logo-smaller.png?alt=media&token=75c0869d-020d-4f75-984f-f29100a173a2' style='display:block' border='0'></a></td></tr></table><!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]--></td></tr><tr><td bgcolor='White' align='center' style='padding:45px 15px 45px 15px;border-top:5px solid rgb(248, 130, 3)' class='section-padding'><!--[if (gte mso 9)|(IE)]><table align='center' border='0' cellspacing='0' cellpadding='0' width='500'><tr><td align='center' valign='top' width='500'><![endif]--><table border='0' cellpadding='0' cellspacing='0' width='100%' style='max-width:500px' class='responsive-table'><tr><td><table width='100%' border='0' cellspacing='0' cellpadding='0'><tr><td><table width='100%' border='0' cellspacing='0' cellpadding='0'><tr><td align='left' style='font-size:25px;font-family:Helvetica,Arial,sans-serif;font-weight:600;color:rgb(51, 51, 51);padding-top:30px' class='padding'>Hi " + name + ",</td></tr><tr><td align='left' style='padding:20px 0 0 0;font-size:16px;line-height:25px;font-family:Helvetica,Arial,sans-serif;color:rgb(52, 58, 64)' class='padding'>You Are Invited To Interview meeting by : <br><br><strong>" + compname + "</strong> <br> Time and Date: On " + date + " at " + time + "<br>Location : " + place + ", <br> Please come to the location, at least 10 minutes early. <br><strong>Cheers,<br>The Mindzzle Team</strong></td></tr></table></td></tr></td></tr></table></td></tr></table></td></tr></table><!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]--></td></tr><tr><td align='center' style='padding:20px 0'><!--[if (gte mso 9)|(IE)]><table align='center' border='0' cellspacing='0' cellpadding='0' width='500'><tr><td align='center' valign='top' width='500'><![endif]--><table width='100%' border='0' cellspacing='0' cellpadding='0' align='center' style='max-width:500px' class='responsive-table'><tr><td align='center' style='font-size:12px;line-height:18px;font-family:Helvetica,Arial,sans-serif;color:black'>Copyright 2018 (c) Mindzzle | Contact | Terms</td></tr></table><!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]--></td></tr></table></div></body></html>"
                  })
        response = {'status': 'Email Sent'}
        email_log(request, mail, "OK", subjects)
        return HttpResponse(response)
    except:
        response = {'status': 'failed to send email'}
        email_log(request, mail, "NOT OK", subjects)
        return HttpResponse(response)


@csrf_exempt
def multidevices_email(request, user, token_phone):
    if settings.FLAG == 0:
        url = 'http://dev-user-api.mindzzle.com/vendor/logoutemail/?token='
    elif settings.FLAG == 1:
        url = 'https://x-user-api.mindzzle.com/vendor/logoutemail/?token='
    elif settings.FLAG == 2:
        url = 'http://staging-user-api.mindzzle.com/vendor/logoutemail/?token='
    elif settings.FLAG == 3:
        url = 'http://127.0.0.1:8000/vendor/logoutemail/?token='

    tad = datetime.datetime.now()
    day = tad.strftime('%c')
    name = user.full_name
    mail = user.email
    subjects = "Multiple Login Alert"
    token = user.token
    url_phone = url + str(token_phone)

    try:
        requests.post(
            "http://email-app.mindzzle.com/mailsent/",
            data={"from": "no-reply@mindzzle.com",
                  "to": mail,
                  "subjects": subjects,
                  "text": "Multiple Login Alert",
                  "html": "<!DOCTYPE html><html xmlns='http://www.w3.org/1999/xhtml' xml:lang='en' lang='en'><head><title>Mindzzle</title><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><meta http-equiv='X-UA-Compatible' content='IE=edge'><style type='text/css'>a,body,table,td{-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%}table,td{mso-table-lspace:0;mso-table-rspace:0}img{-ms-interpolation-mode:bicubic}img{border:0;height:auto;line-height:100%;outline:0;text-decoration:none}table{border-collapse:collapse!important}body{height:100%!important;margin:0!important;padding:0!important;width:100%!important;background-color:rgb(249, 249, 249)}a[x-apple-data-detectors]{color:inherit!important;text-decoration:none!important;font-size:inherit!important;font-family:inherit!important;font-weight:inherit!important;line-height:inherit!important}@media screen and (max-width:525px){.wrapper{width:100%!important;max-width:100%!important}.logo img{margin:0 auto!important}.mobile-hide{display:none!important}.img-max{max-width:100%!important;width:100%!important;height:auto!important}.responsive-table{width:100%!important}.padding{padding:10px 5% 15px 5%!important}.padding-meta{padding:30px 5% 0 5%!important;text-align:center}.padding-copy{padding:10px 5% 10px 5%!important;text-align:center}.no-padding{padding:0!important}.section-padding{padding:50px 15px 50px 15px!important}}div[style*='margin: 16px 0;']{margin:0!important}</style></head><body style='margin:0!important;padding:0!important'><div style='max-width:600px;margin:0 auto' class='responsive-table'><table border='0' cellpadding='0' cellspacing='0' width='100%'><tr><td align='center'><!--[if (gte mso 9)|(IE)]><table align='center' border='0' cellspacing='0' cellpadding='0' width='500'><tr><td align='center' valign='top' width='500'><![endif]--><table border='0' cellpadding='0' cellspacing='0' width='100%' style='max-width:500px' class='wrapper'><tr><td align='center' valign='top' style='padding:15px 0' class='logo'><a href='http://mindzzle.com' target='_blank'><img alt='Logo' src='https://firebasestorage.googleapis.com/v0/b/mindzzle-225411.appspot.com/o/logo_mindzzle%2Ftemplates_mindzzle-logo-smaller.png?alt=media&token=75c0869d-020d-4f75-984f-f29100a173a2' style='display:block' border='0'></a></td></tr></table><!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]--></td></tr><tr><td bgcolor='White' align='center' style='padding:45px 15px 45px 15px;border-top:5px solid rgb(248, 130, 3)' class='section-padding'><!--[if (gte mso 9)|(IE)]><table align='center' border='0' cellspacing='0' cellpadding='0' width='500'><tr><td align='center' valign='top' width='500'><![endif]--><table border='0' cellpadding='0' cellspacing='0' width='100%' style='max-width:500px' class='responsive-table'><tr><td><table width='100%' border='0' cellspacing='0' cellpadding='0'><tr><td><table width='100%' border='0' cellspacing='0' cellpadding='0'><tr><td align='left' style='font-size:25px;font-family:Helvetica,Arial,sans-serif;font-weight:600;color:rgb(51, 51, 51);padding-top:30px' class='padding'>Hi " + name + ",</td></tr><tr><td align='left' style='padding:20px 0 0 0;font-size:16px;line-height:25px;font-family:Helvetica,Arial,sans-serif;color:rgb(52, 58, 64)' class='padding'>We detect someone Login from mobile devices with your account at " + day + ". if it's not you, please press the button below to force logout from all mobile devices</td></tr></table></td></tr><tr><td align='center'><table width='100%' border='0' cellspacing='0' cellpadding='0'><tr><td align='center' style='padding:35px 0 25px 0' class='padding'><table border='0' cellspacing='0' cellpadding='0'><tr><td align='center' style='border-radius:50px' bgcolor='rgb(36, 49, 56)'><a href='" + url_phone + "' target='_blank' style='font-size:16px;font-family:Helvetica,Arial,sans-serif;color:white;text-decoration:none;color:white;text-decoration:none;border-radius:50px;padding:15px 45px;display:inline-block' class='mobile-button'><strong>Logout Mobile Apps</strong></a></td></tr></table></td></tr></table></td></tr><tr><td><table width='100%' border='0' cellspacing='0' cellpadding='0'><tr><td align='left' style='padding:20px 0 0 0;font-size:16px;line-height:25px;font-family:Helvetica,Arial,sans-serif;color:rgb(52, 58, 64)' class='padding'><p>&nbsp;</p><p><strong>Cheers,<br>The Mindzzle Team</strong></p></td></tr></table></td></tr></table></td></tr></table><!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]--></td></tr><tr><td align='center' style='padding:20px 0'><!--[if (gte mso 9)|(IE)]><table align='center' border='0' cellspacing='0' cellpadding='0' width='500'><tr><td align='center' valign='top' width='500'><![endif]--><table width='100%' border='0' cellspacing='0' cellpadding='0' align='center' style='max-width:500px' class='responsive-table'><tr><td align='center' style='font-size:12px;line-height:18px;font-family:Helvetica,Arial,sans-serif;color:black'>Copyright 2018 (c) Mindzzle | Contact | Terms</td></tr></table><!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]--></td></tr></table></div></body></html>"
                  })
        response = {'status': 'Email Sent'}
        email_log(request, mail, "OK", subjects)
        return Response(response)
    except:
        response = {'status': 'failed to send email'}
        email_log(request, mail, "NOT OK", subjects)
        return Response(response)


@csrf_exempt
def reminder_email(request, id_comp):
    # tad = datetime.datetime.now()
    # day = tad.strftime('%c')
    name = id_comp.company_name
    mail = id_comp.email
    subjects = "Your Mindzzle License Is Expired"
    # token = user.token
    # url_phone = url + str(token_phone)

    try:
        requests.post(
            "http://email-app.mindzzle.com/mailsent/",
            data={"from": "admin@mindzzle.com",
                  "to": mail,
                  "subjects": subjects,
                  "text": "License Expired",
                  "html": "<!DOCTYPE html><html xmlns='http://www.w3.org/1999/xhtml' xml:lang='en' lang='en'><head><title>Mindzzle</title><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><meta http-equiv='X-UA-Compatible' content='IE=edge'><style type='text/css'>a,body,table,td{-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%}table,td{mso-table-lspace:0;mso-table-rspace:0}img{-ms-interpolation-mode:bicubic}img{border:0;height:auto;line-height:100%;outline:0;text-decoration:none}table{border-collapse:collapse!important}body{height:100%!important;margin:0!important;padding:0!important;width:100%!important;background-color:rgb(249, 249, 249)}a[x-apple-data-detectors]{color:inherit!important;text-decoration:none!important;font-size:inherit!important;font-family:inherit!important;font-weight:inherit!important;line-height:inherit!important}@media screen and (max-width:525px){.wrapper{width:100%!important;max-width:100%!important}.logo img{margin:0 auto!important}.mobile-hide{display:none!important}.img-max{max-width:100%!important;width:100%!important;height:auto!important}.responsive-table{width:100%!important}.padding{padding:10px 5% 15px 5%!important}.padding-meta{padding:30px 5% 0 5%!important;text-align:center}.padding-copy{padding:10px 5% 10px 5%!important;text-align:center}.no-padding{padding:0!important}.section-padding{padding:50px 15px 50px 15px!important}}div[style*='margin: 16px 0;']{margin:0!important}</style></head><body style='margin:0!important;padding:0!important'><div style='max-width:600px;margin:0 auto' class='responsive-table'><table border='0' cellpadding='0' cellspacing='0' width='100%'><tr><td align='center'><!--[if (gte mso 9)|(IE)]><table align='center' border='0' cellspacing='0' cellpadding='0' width='500'><tr><td align='center' valign='top' width='500'><![endif]--><table border='0' cellpadding='0' cellspacing='0' width='100%' style='max-width:500px' class='wrapper'><tr><td align='center' valign='top' style='padding:15px 0' class='logo'><a href='http://mindzzle.com' target='_blank'><img alt='Logo' src='https://firebasestorage.googleapis.com/v0/b/mindzzle-225411.appspot.com/o/logo_mindzzle%2Ftemplates_mindzzle-logo-smaller.png?alt=media&token=75c0869d-020d-4f75-984f-f29100a173a2' style='display:block' border='0'></a></td></tr></table><!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]--></td></tr><tr><td bgcolor='White' align='center' style='padding:45px 15px 45px 15px;border-top:5px solid rgb(248, 130, 3)' class='section-padding'><!--[if (gte mso 9)|(IE)]><table align='center' border='0' cellspacing='0' cellpadding='0' width='500'><tr><td align='center' valign='top' width='500'><![endif]--><table border='0' cellpadding='0' cellspacing='0' width='100%' style='max-width:500px' class='responsive-table'><tr><td><table width='100%' border='0' cellspacing='0' cellpadding='0'><tr><td><table width='100%' border='0' cellspacing='0' cellpadding='0'><tr><td align='left' style='font-size:25px;font-family:Helvetica,Arial,sans-serif;font-weight:600;color:rgb(51, 51, 51);padding-top:30px' class='padding'>Hi " + name + ",</td></tr><tr><td align='left' style='padding:20px 0 0 0;font-size:16px;line-height:25px;font-family:Helvetica,Arial,sans-serif;color:rgb(52, 58, 64)' class='padding'>We detected your Mindzzle License has Expired, please contact our Administrator at admin@mindzzle.com <br><strong>Cheers,<br>The Mindzzle Team</strong></td></tr></table></td></tr></td></tr></table></td></tr></table></td></tr></table><!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]--></td></tr><tr><td align='center' style='padding:20px 0'><!--[if (gte mso 9)|(IE)]><table align='center' border='0' cellspacing='0' cellpadding='0' width='500'><tr><td align='center' valign='top' width='500'><![endif]--><table width='100%' border='0' cellspacing='0' cellpadding='0' align='center' style='max-width:500px' class='responsive-table'><tr><td align='center' style='font-size:12px;line-height:18px;font-family:Helvetica,Arial,sans-serif;color:black'>Copyright 2018 (c) Mindzzle | Contact | Terms</td></tr></table><!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]--></td></tr></table></div></body></html>"
                  })
        response = {'status': 'Email Sent'}
        email_log(request, mail, "OK", subjects)
        return Response(response)
    except:
        response = {'status': 'failed to send email'}
        email_log(request, mail, "NOT OK", subjects)
        return Response(response)


# @csrf_exempt
# def multidevices_email(request, user):
#   token = '67748e6db2cfd5a87ceb197e7caa581a'
#   url_geo = 'http://api.ipstack.com/check?access_key='
#   req_geo = requests.get(url_geo+token)
#   resp_geo = req_geo.json()
#   negara = resp_geo['country_name']
#   kota = resp_geo['region_name']
#   latitude = resp_geo['latitude']
#   longitude = resp_geo['longitude']
#   latlon = str(latitude)+','+str(longitude)
#   tad = datetime.datetime.now()
#   day = tad.strftime('%c')
#   name = user.full_name
#   mail = user.email
#   subjects = "Multiple Login Alert"
#   token = user.token
#   ip = resp_geo['ip']
#   # payload = {'negara':negara,'kota':kota,'point':latlon,'time':day}
#   try:           
#       requests.post(            
#           "http://email-app.mindzzle.com/mailsent/",
#           data={"from": "no-reply@mindzzle.com",
#                 "to": mail,
#                 "subjects": subjects,
#                 "text": "Multiple Login Alert",
#                 "html": "<!DOCTYPE html><html xmlns='http://www.w3.org/1999/xhtml' xml:lang='en' lang='en'><head><title>Mindzzle</title><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><meta http-equiv='X-UA-Compatible' content='IE=edge'><style type='text/css'>a,body,table,td{-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%}table,td{mso-table-lspace:0;mso-table-rspace:0}img{-ms-interpolation-mode:bicubic}img{border:0;height:auto;line-height:100%;outline:0;text-decoration:none}table{border-collapse:collapse!important}body{height:100%!important;margin:0!important;padding:0!important;width:100%!important;background-color:rgb(249, 249, 249)}a[x-apple-data-detectors]{color:inherit!important;text-decoration:none!important;font-size:inherit!important;font-family:inherit!important;font-weight:inherit!important;line-height:inherit!important}@media screen and (max-width:525px){.wrapper{width:100%!important;max-width:100%!important}.logo img{margin:0 auto!important}.mobile-hide{display:none!important}.img-max{max-width:100%!important;width:100%!important;height:auto!important}.responsive-table{width:100%!important}.padding{padding:10px 5% 15px 5%!important}.padding-meta{padding:30px 5% 0 5%!important;text-align:center}.padding-copy{padding:10px 5% 10px 5%!important;text-align:center}.no-padding{padding:0!important}.section-padding{padding:50px 15px 50px 15px!important}}div[style*='margin: 16px 0;']{margin:0!important}</style></head><body style='margin:0!important;padding:0!important'><div style='max-width:600px;margin:0 auto' class='responsive-table'><table border='0' cellpadding='0' cellspacing='0' width='100%'><tr><td align='center'><!--[if (gte mso 9)|(IE)]><table align='center' border='0' cellspacing='0' cellpadding='0' width='500'><tr><td align='center' valign='top' width='500'><![endif]--><table border='0' cellpadding='0' cellspacing='0' width='100%' style='max-width:500px' class='wrapper'><tr><td align='center' valign='top' style='padding:15px 0' class='logo'><a href='http://mindzzle.com' target='_blank'><img alt='Logo' src='https://firebasestorage.googleapis.com/v0/b/mindzzle-225411.appspot.com/o/logo_mindzzle%2Ftemplates_mindzzle-logo-smaller.png?alt=media&token=75c0869d-020d-4f75-984f-f29100a173a2' style='display:block' border='0'></a></td></tr></table><!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]--></td></tr><tr><td bgcolor='White' align='center' style='padding:45px 15px 45px 15px;border-top:5px solid rgb(248, 130, 3)' class='section-padding'><!--[if (gte mso 9)|(IE)]><table align='center' border='0' cellspacing='0' cellpadding='0' width='500'><tr><td align='center' valign='top' width='500'><![endif]--><table border='0' cellpadding='0' cellspacing='0' width='100%' style='max-width:500px' class='responsive-table'><tr><td><table width='100%' border='0' cellspacing='0' cellpadding='0'><tr><td><table width='100%' border='0' cellspacing='0' cellpadding='0'><tr><td align='left' style='font-size:25px;font-family:Helvetica,Arial,sans-serif;font-weight:600;color:rgb(51, 51, 51);padding-top:30px' class='padding'>Hi "+name+",</td></tr><tr><td align='left' style='padding:20px 0 0 0;font-size:16px;line-height:25px;font-family:Helvetica,Arial,sans-serif;color:rgb(52, 58, 64)' class='padding'>We Detected someone login into your account with a new devices from "+kota+","+negara+" area, at "+day+" , and IP"+ip+". <br><strong>Cheers,<br>The Mindzzle Team</strong></td></tr></table></td></tr></td></tr></table></td></tr></table></td></tr></table><!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]--></td></tr><tr><td align='center' style='padding:20px 0'><!--[if (gte mso 9)|(IE)]><table align='center' border='0' cellspacing='0' cellpadding='0' width='500'><tr><td align='center' valign='top' width='500'><![endif]--><table width='100%' border='0' cellspacing='0' cellpadding='0' align='center' style='max-width:500px' class='responsive-table'><tr><td align='center' style='font-size:12px;line-height:18px;font-family:Helvetica,Arial,sans-serif;color:black'>Copyright 2018 (c) Mindzzle | Contact | Terms</td></tr></table><!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]--></td></tr></table></div></body></html>"
#                 })        
#       response = {'status':'Email Sent'}
#       email_log(request,mail,"OK",subjects)
#       return Response(response)
#   except:
#       response = {'status':'failed to send email'}
#       email_log(request,mail,"NOT OK",subjects)
#       return Response(response)

@csrf_exempt
def vendors_login_alert(request, vendors):
    token = '67748e6db2cfd5a87ceb197e7caa581a'
    url_geo = 'http://api.ipstack.com/check?access_key='
    req_geo = requests.get(url_geo + token)
    resp_geo = req_geo.json()
    negara = resp_geo['country_name']
    kota = resp_geo['region_name']
    latitude = resp_geo['latitude']
    longitude = resp_geo['longitude']
    ip = resp_geo['ip']
    latlon = str(latitude) + ',' + str(longitude)
    tad = datetime.datetime.now()
    day = tad.strftime('%c')
    name = 'admin'
    mail = 'anonying.anonym@gmail.com'
    subjects = "Vendors Login Alert"

    # payload = {'negara':negara,'kota':kota,'point':latlon,'time':day}
    try:
        requests.post(
            "http://email-app.mindzzle.com/mailsent/",
            data={"from": "no-reply@mindzzle.com",
                  "to": mail,
                  "subjects": subjects,
                  "text": "Vendors Login Alert",
                  "html": "<!DOCTYPE html><html xmlns='http://www.w3.org/1999/xhtml' xml:lang='en' lang='en'><head><title>Mindzzle</title><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><meta http-equiv='X-UA-Compatible' content='IE=edge'><style type='text/css'>a,body,table,td{-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%}table,td{mso-table-lspace:0;mso-table-rspace:0}img{-ms-interpolation-mode:bicubic}img{border:0;height:auto;line-height:100%;outline:0;text-decoration:none}table{border-collapse:collapse!important}body{height:100%!important;margin:0!important;padding:0!important;width:100%!important;background-color:rgb(249, 249, 249)}a[x-apple-data-detectors]{color:inherit!important;text-decoration:none!important;font-size:inherit!important;font-family:inherit!important;font-weight:inherit!important;line-height:inherit!important}@media screen and (max-width:525px){.wrapper{width:100%!important;max-width:100%!important}.logo img{margin:0 auto!important}.mobile-hide{display:none!important}.img-max{max-width:100%!important;width:100%!important;height:auto!important}.responsive-table{width:100%!important}.padding{padding:10px 5% 15px 5%!important}.padding-meta{padding:30px 5% 0 5%!important;text-align:center}.padding-copy{padding:10px 5% 10px 5%!important;text-align:center}.no-padding{padding:0!important}.section-padding{padding:50px 15px 50px 15px!important}}div[style*='margin: 16px 0;']{margin:0!important}</style></head><body style='margin:0!important;padding:0!important'><div style='max-width:600px;margin:0 auto' class='responsive-table'><table border='0' cellpadding='0' cellspacing='0' width='100%'><tr><td align='center'><!--[if (gte mso 9)|(IE)]><table align='center' border='0' cellspacing='0' cellpadding='0' width='500'><tr><td align='center' valign='top' width='500'><![endif]--><table border='0' cellpadding='0' cellspacing='0' width='100%' style='max-width:500px' class='wrapper'><tr><td align='center' valign='top' style='padding:15px 0' class='logo'><a href='http://mindzzle.com' target='_blank'><img alt='Logo' src='https://firebasestorage.googleapis.com/v0/b/mindzzle-225411.appspot.com/o/logo_mindzzle%2Ftemplates_mindzzle-logo-smaller.png?alt=media&token=75c0869d-020d-4f75-984f-f29100a173a2' style='display:block' border='0'></a></td></tr></table><!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]--></td></tr><tr><td bgcolor='White' align='center' style='padding:45px 15px 45px 15px;border-top:5px solid rgb(248, 130, 3)' class='section-padding'><!--[if (gte mso 9)|(IE)]><table align='center' border='0' cellspacing='0' cellpadding='0' width='500'><tr><td align='center' valign='top' width='500'><![endif]--><table border='0' cellpadding='0' cellspacing='0' width='100%' style='max-width:500px' class='responsive-table'><tr><td><table width='100%' border='0' cellspacing='0' cellpadding='0'><tr><td><table width='100%' border='0' cellspacing='0' cellpadding='0'><tr><td align='left' style='font-size:25px;font-family:Helvetica,Arial,sans-serif;font-weight:600;color:rgb(51, 51, 51);padding-top:30px' class='padding'>Hi " + name + ",</td></tr><tr><td align='left' style='padding:20px 0 0 0;font-size:16px;line-height:25px;font-family:Helvetica,Arial,sans-serif;color:rgb(52, 58, 64)' class='padding'>" + vendors + " login from " + kota + "," + negara + " area, at " + day + " , and IP" + ip + ". <br><strong>Cheers,<br>The Mindzzle Team</strong></td></tr></table></td></tr></td></tr></table></td></tr></table></td></tr></table><!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]--></td></tr><tr><td align='center' style='padding:20px 0'><!--[if (gte mso 9)|(IE)]><table align='center' border='0' cellspacing='0' cellpadding='0' width='500'><tr><td align='center' valign='top' width='500'><![endif]--><table width='100%' border='0' cellspacing='0' cellpadding='0' align='center' style='max-width:500px' class='responsive-table'><tr><td align='center' style='font-size:12px;line-height:18px;font-family:Helvetica,Arial,sans-serif;color:black'>Copyright 2018 (c) Mindzzle | Contact | Terms</td></tr></table><!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]--></td></tr></table></div></body></html>"
                  })
        response = {'status': 'Email Sent'}
        email_log(request, mail, "OK", subjects)
        return Response(response)
    except:
        response = {'status': 'failed to send email'}
        email_log(request, mail, "NOT OK", subjects)
        return Response(response)


@api_view(['GET'])
def email_get(request):
    if request.method == 'GET':
        network = Email.objects.all()
        serializer = EmailSerializer(network, many=True)
        return Response(serializer.data)
