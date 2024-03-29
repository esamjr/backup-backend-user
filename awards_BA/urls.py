from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/(?P<pk>[0-9]+)$', views.get_delete_update_award, name='get_delete_update_award'),
    url(r'^api/$', views.get_post_award, name='get_post_award'),
    url(r'^api/user/(?P<pk>[0-9]+)$', views.get_post_award_user, name='get_post_award_user'),
]