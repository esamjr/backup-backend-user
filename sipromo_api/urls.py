from django.conf.urls import url
from . import views
# from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [ 
	url(r'^api/voucher/(?P<stri>[a-zA-Z0-9]+)$',  views.sipromo, name='sipromo'),
	
]