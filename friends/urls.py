from django.urls import path
from . import views

urlpatterns = [
    # watcher!
    path('', views.watcher, name='watcher'),

    # search base on name
    path('search/<int:user_id>/<str:name>', views.search, name="search"),

    # get friend suggestion of the designated user
    path('friendsuggestion/<int:id>', views.friendsuggestion, name='friendsuggestion'),

    # get friend list of the designated user
    path('friendlist/<int:id>', views.friend_list, name='friend_list'),

    # get friend request of the designated user 
    path('request/<int:id>', views.friend_request, name='friend_request'),

    # User Cancelled friend request
    path('request/cancel/<int:user_id>', views.cancel_friend_request, name='cancel_friend_request'),

    # request for a new friend
    path('request/add/<int:user_id>/<int:friend_id>', views.add_friend, name='add_friend'),

    # ignore friend request
    path('request/ignore/<int:user_id>/<int:friend_id>', views.ignore_friend, name='ignore_friend'),

    # accept friend request
    path('request/accept/<int:user_id>/<int:friend_id>', views.accept_friend, name='accept_friend'),

    # unfriend
    path('unfriend/<int:user_id>/<int:friend_id>', views.unfriend, name='unfriend'),

    ]
