from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/(?P<pk>[0-9]+)$', views.get_delete_update_usertype, name='get_delete_update_usertype'),
    url(r'^api/$', views.get_post_usertype, name='get_post_usertype'),
]