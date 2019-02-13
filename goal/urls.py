from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/(?P<pk>[0-9]+)$', views.get_put_delete, name='get_put_delete'),
    url(r'^api/$', views.post_get_goals, name='post_get_goals'),
    # url(r'^api/filter/(?P<pk1>[0-9]+)/(?P<pk2>[0-9]+)$', views.get_all_hierarchy, name='get_all_hierarchy'),
]
