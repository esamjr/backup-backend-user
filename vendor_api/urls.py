from django.conf.urls import url
from . import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [ 
	url(r'^api/$',  views.generate, name='generate'),
	url(r'^api-token-auth/', obtain_jwt_token, name='obtain'),
]