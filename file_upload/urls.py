from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^api/upload/$', views.upload_file, name='upload_file'),
    # url(r'^api/$', views.email_get, name='email_get'),
]