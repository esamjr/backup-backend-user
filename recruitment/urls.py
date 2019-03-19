from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^api/jobs/$', views.get_post_jobs, name='get_post_jobs'),
	url(r'^api/(?P<pk>[0-9]+)$', views.get_delete_put_jobs, name='get_delete_put_jobs'),
	url(r'^api/apply/(?P<pk>[0-9]+)$', views.apply, name='apply'),
	url(r'^api/searchrecruitment/(?P<pk>[0-9]+)$', views.search_by_id_rec, name='search_by_id_rec'),
	url(r'^api/search/(?P<pk>[0-9]+)$', views.search, name='search'),

]