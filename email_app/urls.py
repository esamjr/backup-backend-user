from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/sendmail/$', views.send_simple_message, name='send_simple_message'),
    url(r'^api/$', views.email_get, name='email_get'),
]