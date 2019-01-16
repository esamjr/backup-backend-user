from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/v1/message/(?P<pk>[0-9]+)$', views.get_delete_update_message, name='get_delete_update_message'),
    url(r'^api/v1/message/$', views.get_post_message, name='get_post_message'),
]