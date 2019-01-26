from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/(?P<pk>[0-9]+)$', views.get_delete_update_businessaccount, name='get_delete_update_businessaccount'),
    url(r'^api/$', views.get_post_businessaccount, name='get_post_businessaccount'),    
    url(r'^api/filter/(?P<pk>[0-9]+)$', views.get_all_businessaccount, name='get_all_businessaccount'),
    url(r'^api/search/$', views.search_company, name = 'search_company'),
    url(r'^api/custom/(?P<pk>[0-9]+)$', views.custom_get_all_businessaccount, name='custom_get_all_businessaccount')
]
