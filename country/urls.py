from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/v1/country/(?P<pk>[0-9]+)$', views.get_delete_update_country, name='get_delete_update_country'),
    url(r'^api/v1/country/$', views.get_post_country, name='get_post_country'),
]