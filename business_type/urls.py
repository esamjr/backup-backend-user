from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/(?P<pk>[0-9]+)$', views.get_delete_update_businesstype, name='get_delete_update_businesstype'),
    url(r'^api/$', views.get_post_businesstype, name='get_post_businesstype'),
    url(r'^api/filter/(?P<pk>[0-9]+)$', views.get_all_businesstype, name='get_all_businesstype'),
]
