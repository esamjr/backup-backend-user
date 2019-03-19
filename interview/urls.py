from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^api/(?P<pk>[0-9]+)$', views.get_put_delete_interview, name='get_put_delete_interview'),
    url(r'^api/$', views.get_post_interview, name='get_post_interview'),

]
