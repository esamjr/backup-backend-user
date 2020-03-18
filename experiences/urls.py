from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/(?P<pk>[0-9]+)$', views.get_delete_update_experiences, name='get_delete_update_experiences'),
    url(r'^api/$', views.get_post_experiences, name='get_post_experiences'),
    url(r'^api/user/$', views.get_post_experiences_user, name='get_post_experiences_user'),
]
