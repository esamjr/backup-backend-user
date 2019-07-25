from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/$', views.get_post_catgoal, name='get_post_catgoal'),
    url(r'^api/(?P<pk>[0-9]+)$', views.get_put_delete, name='get_put_delete'),
]
