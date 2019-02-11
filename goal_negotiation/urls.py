from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/$', views.goal_nego, name='goal_nego'),
    # url(r'^api/filter/(?P<pk1>[0-9]+)/(?P<pk2>[0-9]+)$', views.get_all_hierarchy, name='get_all_hierarchy'),
]
