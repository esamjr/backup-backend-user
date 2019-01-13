from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/(?P<pk>[0-9]+)$', views.get_delete_update_typetime, name='get_delete_update_typetime'),
    url(r'^api/$', views.get_post_typetime, name='get_post_typetime'),
    url(r'^api/user/(?P<pk>[0-9]+)$', views.get_post_typetime_user, name='get_post_typetime_user'),
]