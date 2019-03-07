from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^api/getbycompany/(?P<pk>[0-9]+)$', views.get_type_by_company, name='get_type_by_company'),
    url(r'^api/$', views.tipe_goal, name='tipe_goal'),
]
