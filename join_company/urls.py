from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^api/joinbyuseractive/(?P<pk>[0-9]+)$', views.join_company_by_active, name='join_company_by_active'),
    url(r'^api/(?P<pk>[0-9]+)$', views.get_delete_update_joincompany, name='get_delete_update_joincompany'),
    url(r'^api/$', views.get_post_joincompany, name='get_post_joincompany'),
    url(r'^server/$', views.server_integration, name='server_integration'),
    url(r'^api/user/(?P<pk>[0-9]+)$', views.get_post_joincompany_user, name='get_post_joincompany_user'),
]
