from django.urls import path
from . import views

urlpatterns = [
    # get-post feed
    path('', views.get_post_feed),
    # put-delete feed
    path('update/', views.put_delete_feed),
    # get all-likes
    path('likes/', views.likes),
    # get feed-like-count
    path('likes/count/', views.feed_likes_count),
    # put like
    # path('<int:id>/likes/<int:user_id>', views.like),
    path('like/', views.like),
    # put unlike
    # path('<int:id>/unlike/<int:user_id>', views.unlike),
    path('unlike/', views.unlike),
    # get all-comment
    path('comments/', views.get_post_comment),
    # get feed-comment count
    path('comments/count/', views.comment_feed_count),
    # put-delete comment
    path('comments/update/', views.put_delete_comment),

    path('object/', views.feed_object),
]
