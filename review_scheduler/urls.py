from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^api/getbycompany/(?P<pk>[0-9]+)$', views.get_review_by_company, name='get_review_by_company'),
    url(r'^api/$', views.revies_sched, name='revies_sched'),
]
