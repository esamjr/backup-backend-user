from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/resendemail/$', views.resend_email, name='resend_email'),
    url(r'^api/sendmail/$', views.send_email, name='send_email'),
    url(r'^api/$', views.email_get, name='email_get'),
]
