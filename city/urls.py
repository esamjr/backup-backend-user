from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/(?P<pk>[0-9]+)$', views.get_delete_update_city, name='get_delete_update_city'),
    url(r'^api/$', views.get_post_city, name='get_post_city'),
    url(r'^api/(?P<pk1>[0-9]+)/(?P<pk2>[0-9]+)$', views.get_post_region, name='get_post_region'),
]