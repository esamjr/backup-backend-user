from django.urls import path
from . import views

urlpatterns = [
    # watcher!
    path('', views.watcher, name='watcher'),
    # get list of specific-user-friends
    path('list/', views.user_friends_list, name='user_friends_list'),
    # get friend-request for specific-user
    path('request/', views.friend_request, name='friend_request'),
    # get list of user-friends-request
    path('request/list/', views.friend_request_list, name='friend_request_list'),
    # put add-friend
    path('request/add/', views.add_friend, name='add_friend'),
    # put user cancelled-friend-request
    path('request/cancel/', views.cancel_friend_request, name='cancel_friend_request'),
    # put user ignore-friend-request
    path('request/ignore/', views.ignore_request, name='ignore_request'),
    # put user accept-friend-request
    path('request/accept/', views.accept_request, name='accept_request'),
    # put user unfriend user-friend
    path('unfriend/', views.unfriend, name='unfriend'),
    # get user blocked-user-list
    path('block/list/', views.blocked_list, name='blocked_list'),
    # put user block-friend-request
    path('block/add/', views.block_user, name='block_user'),

    # get friend-suggestion for specific-user
    path('suggestions/', views.suggestions, name='suggestions'),
    # search base on name
    path('search/<int:id>/<str:name>', views.search, name="search"),
]

