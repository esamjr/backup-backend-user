from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/(?P<pk>[0-9]+)$', views.get_delete_update_region, name='get_delete_update_region'),
    url(r'^api/$', views.get_post_region, name='get_post_region'),
    url(r'^api/country/(?P<pk>[0-9]+)$', views.get_post_region_country, name='get_post_region_country'),
]