from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/(?P<pk>[0-9]+)$', views.get_delete_update_registrations, name='get_delete_update_registrations'),
    url(r'^api/$', views.get_post_registrations, name='get_post_registrations'),
    url(r'^api/login/$', views.get_login, name='get_login'),
]