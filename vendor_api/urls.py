from django.conf.urls import url
from . import views
# from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [ 
	url(r'^api/api_login_absensee/$', views.api_login_absensee, name='api_login_absensee'),
	url(r'^api/api_find_company_absensee/$', views.api_find_company_absensee, name='api_find_company_absensee'),
	url(r'^api/login_out/$',  views.login_logout_vendors, name='login_logout_vendors'),
	url(r'^api/$',  views.generate, name='generate'),
	# url(r'^api-token-auth/', obtain_jwt_token, name='obtain'),
]