from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/(?P<pk>[0-9]+)$', views.get_delete_update_historyhierarchy, name='get_delete_update_historyhierarchy'),
    url(r'^api/filter/$', views.get_all_historyhierarchy, name='get_all_historyhierarchy'),
    url(r'^api/$', views.get_post_historyhierarchy, name='get_post_historyhierarchy'),
]
