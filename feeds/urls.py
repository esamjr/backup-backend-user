from django.urls import path
from . import views

urlpatterns = [
    # get-post feed
    path('', views.get_post_feed),
    # put-delete feed
    path('<int:id>', views.put_delete_feed),
    # get all-likes
    path('likes', views.likes),
    # get specific-user-like
    path('likes/<int:user_id>', views.user_feed_likes),
    # get feed-like-count
    path('<int:id>/likes/count', views.feed_likes_count),
    # put like
    # path('likes/<int:id>/feed/<int:feed_id>', views.like),
    path('<int:id>/likes/<int:user_id>', views.like),
    # put unlike
    # path('unlike/<int:id>/feed/<int:feed_id>', views.unlike),
    path('<int:id>/unlike/<int:user_id>', views.unlike),
    # get all-comment
    path('comments', views.get_post_comment),
    # get feed-comment count
    path('<int:id>/comments/count', views.comment_feed_count),
    # put-delete comment
    path('comments/<int:id>', views.put_delete_comment),

    path('object', views.feed_object),
]
