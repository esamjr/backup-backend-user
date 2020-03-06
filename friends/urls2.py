from django.conf.urls import url
from . import views2

urlpatterns = [
    # watcher!
    url(r'^api/$', views.watcher, name='watcher'),

    # search base on name
    url(r'^api/search/(?P<pk>[0-9]+)/(?P<name>[a-zA-z%]+)$', views.search, name="search"),

    # get friend suggestion of the designated user
    url(r'^api/friendsuggestion/(?P<pk>[0-9]+)$', views.friendsuggestion, name='friendsuggestion'),

    # get friend list of the designated user
    url(r'^api/friendlist/(?P<pk>[0-9]+)$', views.friendlist, name='friendlist'),

    # get friend request of the designated user 
    url(r'^api/request/(?P<pk>[0-9]+)$', views.friend_request, name='friend_request'),

    # request for a new friend
    url(r'^api/request/add/(?P<user_pk>[0-9]+)/(?P<friend_pk>[0-9]+)$', views.add_friend, name='add_friend'),

    # ignore friend request
    url(r'^api/request/ignore/(?P<user_pk>[0-9]+)/(?P<friend_pk>[0-9]+)$', views.ignore_friend, name='ignore_friend'),

    # accept friend request
    url(r'^api/request/accept/(?P<user_pk>[0-9]+)/(?P<friend_pk>[0-9]+)$', views.accept_friend, name='accept_friend'),

    # unfriend
    url(r'^api/unfriend/(?P<user_pk>[0-9]+)/(?P<friend_pk>[0-9]+)$', views.unfriend, name='unfriend'),

    ]
