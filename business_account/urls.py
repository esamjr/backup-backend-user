from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/get-all-emp-by-id-comp/(?P<pk>[0-9]+)$', views.get_all_emp_by_id_comp, name='get_all_emp_by_id_comp'),
    url(r'^api/get-all-comp/$', views.get_all_name_id_comp, name='get_all_name_id_comp'), 
    url(r'^api/verified_company/$', views.verfied_business, name='verfied_business'), 
    url(r'^api/empbabyusers/$', views.get_ba_by_users, name='get_ba_by_users'),    
	url(r'^vendoronly/getchild/(?P<pk>[0-9]+)$', views.child_company_vendor, name='child_company_vendor'),
	url(r'^vendoronly/(?P<pk>[0-9]+)$', views.buat_vendor, name='buat_vendor'),
	url(r'^vendoronly/findcuremployee/(?P<pk>[0-9]+)$', views.cakarsebek_vendor, name='cakarsebek_vendor'),
    url(r'^api/(?P<pk>[0-9]+)$', views.get_delete_update_businessaccount, name='get_delete_update_businessaccount'),
    url(r'^api/$', views.get_post_businessaccount, name='get_post_businessaccount'),    
    url(r'^api/comp_bio/(?P<pk>[0-9]+)$', views.count_emp, name='count_emp'),
    url(r'^api/filter/(?P<pk>[0-9]+)$', views.get_all_businessaccount, name='get_all_businessaccount'),
    url(r'^api/search/$', views.search_company, name = 'search_company'),
    url(r'^api/custom/apply/(?P<pk>[0-9]+)$', views.custom_get_one, name='custom_get_one'),
    url(r'^api/findcuremployee/(?P<pk>[0-9]+)$', views.cakarsebek, name='cakarsebek'),
    url(r'^api/get_name/(?P<pk>[0-9]+)$', views.get_name, name='get_name'),
    url(r'^api/custom/active/(?P<pk>[0-9]+)$', views.custom_get_two, name='custom_get_two'),

    # new api
    url(r'^api/get_list_employee/$', views.get_employee_by_id_comp, name='get_employee_by_id'),

    # api for crocodic
    url(r'^api/get_employee/(?P<pk>[0-9]+)$', views.get_data_employee, name='get_data_employee'),
]
