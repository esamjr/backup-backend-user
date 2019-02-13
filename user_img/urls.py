from django.conf.urls import url
from . import views

urlpatterns = [
    
    url(r'^api/$', views.upload_doc, name='upload_doc'),
   
]