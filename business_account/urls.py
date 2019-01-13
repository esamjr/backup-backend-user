from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/(?P<pk>[0-9]+)$', views.get_delete_update_businessaccount, name='get_delete_update_businessaccount'),
    url(r'^api/$', views.get_post_businessaccount, name='get_post_businessaccount'),    
    url(r'^api/filter/(?P<pk>[0-9]+)$', views.get_all_businessaccount, name='get_all_businessaccount'),
   
]
