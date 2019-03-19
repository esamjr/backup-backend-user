from django.conf.urls import url
from . import views

urlpatterns = [	
	url(r'^api/(?P<pk>[0-9]+)$', views.post_get_jobfair_by_comp, name='post_get_jobfair_by_comp'),
	url(r'^api/getbycomp/(?P<pk>[0-9]+)$', views.get_one_jobfair, name='get_one_jobfair'),

]