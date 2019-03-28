from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/sendmail/$', views.send_email, name='send_email'),
    url(r'^api/$', views.email_get, name='email_get'),
    url(r'^testing/$', views.percobaan, name='percobaan'),
]