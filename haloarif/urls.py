from django.conf.urls import url
from . import views
# from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [ 
	url(r'^api/(?P<string>[a-zA-Z0-9]+)/$',  views.api_haloarif, name='api_haloarif'),
	
]