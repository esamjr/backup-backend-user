from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/v1/role_type/(?P<pk>[0-9]+)$', views.get_delete_update_roletype, name='get_delete_update_roletype'),
    url(r'^api/v1/role_type/$', views.get_post_roletype, name='get_post_roletype'),
]