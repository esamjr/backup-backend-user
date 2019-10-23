from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^api/(?P<pk>[0-9]+)$', views.get_delete_update_experiences, name='get_delete_update_experiences'),
    url(r'^api/$', views.get_post_delete_feeds, name='get_post_delete_feeds_api'),
    url(r'^api/put/(?P<pk>[0-9]+)$', views.put_feeds, name='put_feeds_api'),

    # likes watcher
    url(r'^api/likes/$', views.likes, name="likes"),

    # likes specific watcher
    url(r'^api/likes/(?P<pk>[0-9]+)$', views.likes_specific, name="likes_specific"),

    # create new likes object
    url(r'^api/likes/create/$', views.likes_create, name="likes_create"),

    # add new feeds you like
    url(r'^api/likes/like/(?P<user_pk>[0-9]+)/(?P<feeds_pk>[0-9]+)$', views.likes_like, name="likes_like"),

    # unfo feeds you like
    url(r'^api/likes/unlike/(?P<user_pk>[0-9]+)/(?P<feeds_pk>[0-9]+)$', views.likes_unlike, name="likes_unlike"),

    # see how many likes in feeds
    url(r'^api/likes/count/(?P<feeds_pk>[0-9]+)$', views.likes_count, name="likes_count"),

    # comments watcher
    url(r'^api/comments/$', views.comments, name='comments'),

    # comments specific watcher
    url(r'^api/comments/(?P<pk>[0-9]+)$', views.comments_specific, name='comments_specific'),

    # see how many comments in feeds
    url(r'^api/comments/count/(?P<feeds_pk>[0-9]+)$', views.comments_count, name="comments_count"),


]
