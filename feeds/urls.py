from django.urls import path
from . import views

urlpatterns = [
    # show-create feed
    path('', views.get_post_feeds),
    # edit-delete feed
    path('<int:feed_id>', views.put_delete_feed),
    # show likes
    path('likes/', views.show_likes),
    # show specific-likes
    path('likes/<int:user_id>', views.specific_user_like),
    # show feed-likes-count
    path('likes/count/<int:feed_id>', views.liked_feed),
    # edit: like
    path('likes/<int:user_id>/<int:feed_id>', views.like),
    # edit: unlike
    path('unlike/<int:user_id>/<int:feed_id>', views.unlike),
    # show-create comment
    path('comments/', views.get_post_comments),
    # show specific-feed-comment
    path('<int:feed_id>/comments/', views.specific_feed_comment),
    # show specific feeds-comment-count
    path('comments/count/<int:feed_id>', views.comments_count),
    # delete comment
    path('comments/<int:comment_id>', views.edit_delete_comment),
]
