from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/(?P<pk>[0-9]+)$', views.get_delete_update_level, name='get_delete_update_level'),
    url(r'^api/$', views.get_post_level, name='get_post_level'),
    url(r'^api/comp_filter/(?P<pk>[0-9]+)$', views.filter_comp, name='filter_comp'),
]