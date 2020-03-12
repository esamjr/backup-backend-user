from django.urls import path
from . import views

urlpatterns = [
    # watcher!
    path('', views.watcher, name='watcher'),
    # get specific-user-friends-list
    path('friendlist/', views.user_friends_list, name='user_friends_list'),
    # get friend suggestion of the designated user
    path('friendsuggestion/', views.friendsuggestion, name='friendsuggestion'),

    # search base on name
    path('search/<int:user_id>/<str:name>', views.search, name="search"),



    # get friend request of the designated user
    path('request/', views.friend_request, name='friend_request'),

    # get history friend request send
    path('request/list/', views.friend_request_list, name='friend_request_list'),

    # User Cancelled friend request
    path('request/cancel/', views.cancel_friend_request,
         name='cancel_friend_request'),

    # request for a new friend
    path('request/add/', views.add_friend, name='add_friend'),

    # ignore friend request
    path('request/ignore/', views.ignore_friend, name='ignore_friend'),

    # accept friend request
    path('request/accept/', views.accept_friend, name='accept_friend'),

    # unfriend
    path('unfriend/', views.unfriend, name='unfriend'),
]
