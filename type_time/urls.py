from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/v1/typetime/(?P<pk>[0-9]+)$', views.get_delete_update_typetime, name='get_delete_update_typetime'),
    url(r'^api/v1/typetime/$', views.get_post_typetime, name='get_post_typetime'),
]