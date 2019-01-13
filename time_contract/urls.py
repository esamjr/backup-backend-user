from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/(?P<pk>[0-9]+)$', views.get_delete_update_timecontract, name='get_delete_update_timecontract'),
    url(r'^api/filter/(?P<pk>[0-9]+)$', views.get_all_timecontract, name='get_all_timecontract'),
    url(r'^api/$', views.get_post_timecontract, name='get_post_timecontract'),
]