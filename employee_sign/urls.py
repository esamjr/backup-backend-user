from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/(?P<pk>[0-9]+)$', views.get_delete_update_employeesign, name='get_delete_update_employeesign'),
    url(r'^api/filter/(?P<pk1>[0-9]+<pk1>[0-9])$', views.get_all_employeesign, name='get_all_employeesign'),
    url(r'^api/$', views.get_post_employeesign, name='get_post_employeesign'),
]
