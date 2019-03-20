from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/personalchat/(?P<pk>[0-9]+)$', views.get_post_pchat, name='get_post_pchat'),
    url(r'^api/groupchat/(?P<pk>[0-9]+)$', views.get_post_gchat, name='get_post_gchat'),
    url(r'^api/addmembers/(?P<pk>[0-9]+)$', views.adding_members, name='adding_members'),
    url(r'^api/deletechat/(?P<pk>[0-9]+)$', views.delete_message, name='delete_message'),
    # url(r'^api/(?P<pk>[0-9]+)$', views.get_put_delete_interview, name='get_put_delete_interview'),
    # url(r'^api/$', views.get_post_interview, name='get_post_interview'),

]
