from django.conf.urls import url
from . import views

urlpatterns = [	
	url(r'^api/(?P<pk>[0-9]+)$', views.get_post_testform, name='get_post_testform'),
	url(r'^api/getandedit/(?P<pk>[0-9]+)$', views.get_put_delete_test, name='get_put_delete_test'),
	# url(r'^api/getbyjobs/(?P<pk>[0-9]+)$', views.get_test_by_jobs, name='get_test_by_jobs'),
	url(r'^api/postansw/(?P<pk>[0-9]+)$', views.testans_forms, name='testans_forms'),
	url(r'^api/answer/$', views.answer, name='answer'),	
	url(r'^api/score/(?P<pk>[0-9]+)$', views.print_score, name='print_score'),
]