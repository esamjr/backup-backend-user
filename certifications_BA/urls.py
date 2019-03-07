from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/(?P<pk>[0-9]+)$', views.get_delete_update_certification, name='get_delete_update_certification'),
    url(r'^api/$', views.get_post_certification, name='get_post_certification'),
    url(r'^api/user/(?P<pk>[0-9]+)$', views.get_post_certification_user, name='get_post_certification_user'),
]