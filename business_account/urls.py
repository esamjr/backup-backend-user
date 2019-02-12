from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^vendoronly/(?P<pk>[0-9]+)$', views.buat_vendor, name='buat_vendor'),
	url(r'^vendoronly/findcuremployee/(?P<pk>[0-9]+)$', views.cakarsebek_vendor, name='cakarsebek_vendor'),
    url(r'^api/(?P<pk>[0-9]+)$', views.get_delete_update_businessaccount, name='get_delete_update_businessaccount'),
    url(r'^api/$', views.get_post_businessaccount, name='get_post_businessaccount'),    
    url(r'^api/comp_bio/(?P<pk>[0-9]+)$', views.count_emp, name='count_emp'),
    url(r'^api/filter/(?P<pk>[0-9]+)$', views.get_all_businessaccount, name='get_all_businessaccount'),
    url(r'^api/search/$', views.search_company, name = 'search_company'),
    url(r'^api/custom/apply/(?P<pk>[0-9]+)$$', views.custom_get_one, name='custom_get_one'),
    url(r'^api/findcuremployee/(?P<pk>[0-9]+)$', views.cakarsebek, name='cakarsebek'),
    url(r'^api/custom/active/(?P<pk>[0-9]+)$$', views.custom_get_two, name='custom_get_two')
]
