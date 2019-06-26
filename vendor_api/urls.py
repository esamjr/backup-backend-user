from django.conf.urls import url
from . import views
# from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [ 
	url(r'^api/search/(?P<stri>[a-zA-Z0-9]+)$',  views.search_by_token, name='search_by_token'),
	url(r'^api/checktoken/$',  views.check_token, name='check_token'),
	url(r'^api/migratemultidevice/(?P<pk>[0-9]+)$',  views.migrate_multiuser_company, name='migrate_multiuser_company'),
	url(r'^api/adminattendance/$',  views.check_admin_attendace, name='check_admin_attendace'),
	url(r'^api/clonedatamindzzle/$',  views.cloning_data_reprime, name='cloning_data_reprime'),
	url(r'^api/dashboardreprime/$',  views.timesheets_absensee, name='timesheets_absensee'),
	url(r'^api/businesspayroll/(?P<pk>[0-9]+)$',  views.api_payroll, name='api_payroll'),
	url(r'^api/changeuserstatus/$',  views.change_status_domoo_user, name='change_status_domoo_user'),
	url(r'^api/logindomoo/$',  views.login_logout_domoo, name='login_logout_domoo'),
	url(r'^api/verifyotpdomoo/$',  views.verify_otp_domoo, name='verify_otp_domoo'),
	url(r'^api/forgetpassdomoo/$',  views.forget_passcode_domoo, name='forget_passcode_domoo'),
	url(r'^api/setpasscodedomoo/$',  views.set_passcode_domoo, name='set_passcode_domoo'),
	url(r'^api/registrations_domoo/$',  views.registrations_domoo, name='registrations_domoo'),
	url(r'^api/checkuserdomoo/$',  views.check_user_domoo, name='check_user_domoo'),
	url(r'^api/api_login_absenseev2/(?P<pk>[0-9]+)$', views.api_login_absensee_v2, name='api_login_absensee_v2'),
	url(r'^api/api_login_absensee/$', views.api_login_absensee, name='api_login_absensee'),
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
	url(r'^api/checkhierarchy/$',  views.check_hierarchy, name='check_hierarchy'),

	# url(r'^api-token-auth/', obtain_jwt_token, name='obtain'),
]