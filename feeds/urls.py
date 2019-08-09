from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^api/(?P<pk>[0-9]+)$', views.get_delete_update_experiences, name='get_delete_update_experiences'),
    url(r'^api/$', views.get_post_delete_feeds, name='get_post_delete_feeds_api'),
    url(r'^api/put/(?P<pk>[0-9]+)$', views.put_feeds, name='put_feeds_api'),
    url(r'^api/likesncomments/$', views.get_post_delete_likesncomments, name='api_likesncomments'),
    url(r'^api/likesncomments/specific/(?P<pk>[0-9]+)$', views.get_post_specific_likesncomments, name='get_post_api_specific_likesncomments'),
    # likes api
    url(r'^api/likes/put/add/(?P<user_pk>[0-9]+)/(?P<feedsobj_pk>[0-9]+)$', views.put_add_likes, name="put_add_likes"),
    url(r'^api/likes/put/delete/(?P<user_pk>[0-9]+)/(?P<feedsobj_pk>[0-9]+)$', views.put_delete_likes, name="put_delete_likes"),
    url(r'^api/likes/get/$', views.get_likes, name="get_likes"),
    url(r'^api/likes/get/(?P<pk>[0-9]+)$', views.get_specific_likes, name="get_likes"),
    url(r'^api/likes/post/$', views.post_likes, name="post_likes"),

]
