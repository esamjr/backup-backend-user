from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/(?P<pk>[0-9]+)$', views.get_delete_update_contact, name='get_delete_update_contact'),
    url(r'^api/$', views.get_post_contact, name='get_post_contact'),
    url(r'^api/user/(?P<pk>[0-9]+)$', views.get_post_contact_user, name='get_post_contact_user'),
]
