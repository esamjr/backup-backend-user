from django.conf.urls import url
from . import views

urlpatterns = [ 
    url(r'^api/search/(?P<stri>[a-zA-Z0-9]+)$',  views.search_by_token, name='search_by_token'),
    url(r'^api/checktoken/$',  views.check_token, name='check_token'),
    url(r'^api/migratemultidevice/(?P<pk>[0-9]+)$',  views.migrate_multiuser_company, name='migrate_multiuser_company'),
    url(r'^api/adminattendance/',  views.check_admin_attendace, name='check_admin_attendace'),
	url(r'^api/dashboardreprime/$',  views.timesheets_absensee, name='timesheets_absensee'),
	url(r'^api/api_login_absenseev2/(?P<pk>[0-9]+)$', views.api_login_absensee_v2, name='api_login_absensee_v2'),
	# url(r'^api/api_login_absensee/$', views.api_login_absensee, name='api_login_absensee'),
	url(r'^api/api_find_company_absensee/$', views.api_find_company_absensee, name='api_find_company_absensee'),
	url(r'^api/login_out/$',  views.login_logout_vendors, name='login_logout_vendors'),
	url(r'^api/$',  views.generate, name='generate'),
	url(r'^api/syncbilling/$',  views.sync_billing, name='sync_billing'),
	url(r'^api/syncpayroll/$',  views.sync_emp_config, name='sync_emp_config'),
	url(r'^logoutemail/$',  views.logout_by_email, name='logout_by_email'),
	url(r'^Sendblast/$',  views.send_blast, name='send_blast'),
	url(r'^Sendforgetblast/$',  views.email_forget_blast, name='email_forget_blast'),
	url(r'^download/$',  views.download_data, name='download_data'),
	url(r'^api/empcred/$',  views.employee_cred, name='employee_cred'),
	url(r'^api/checkhierarchy/(?P<pk>[0-9]+)$',  views.check_hierarchy, name='check_hierarchy'),


    # new api
    url(r'^api/api_login_absensee/$', views.login_absensee_views, name='login_absensee_views'),
    url(r'^api/get_employee_by_comp/$', views.get_data_employee, name='get_data_employee'),
    url(r'^api/employee_payroll/$', views.get_data_payroll, name='get_data_payroll'),
]