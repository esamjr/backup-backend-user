from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/(?P<pk>[0-9]+)$', views.get_delete_update_friendlist, name='get_delete_update_friendlist'),
    url(r'^api/$', views.get_post_friendlist, name='get_post_friendlist'),
    url(r'^api/searchall/(?P<pk>[0-9]+)$', views.search_all, name='search_all'),
]
