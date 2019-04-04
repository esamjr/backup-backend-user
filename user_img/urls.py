from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^api/$', views.upload_doc, name='upload_doc'),
    url(r'^api/getalldocs/$', views.get_all_doc, name='get_all_doc'),
    url(r'^api/getthedoc/$', views.get_doc, name='get_doc'),
   
]