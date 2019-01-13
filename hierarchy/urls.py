from django.conf.urls import url
from . import views

urlpatterns = [

	url(r'^api/filter/(?P<pk1>[0-9]+)$', views.get_all_hierarchy, name='get_all_hierarchy'),
    url(r'^api/(?P<pk>[0-9]+)$', views.get_delete_update_hierarchy, name='get_delete_update_hierarchy'),
    url(r'^api/$', views.get_post_hierarchy, name='get_post_hierarchy'),
    # url(r'^api/filter/(?P<pk1>[0-9]+)/(?P<pk2>[0-9]+)$', views.get_all_hierarchy, name='get_all_hierarchy'),
]
