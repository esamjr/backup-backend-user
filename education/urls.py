from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/(?P<pk>[0-9]+)$', views.get_delete_update_education, name='get_delete_update_education'),
    url(r'^api/$', views.get_post_education, name='get_post_education'),
    url(r'^api/user/(?P<pk>[0-9]+)$', views.get_post_education_user, name='get_post_education_user'),

]