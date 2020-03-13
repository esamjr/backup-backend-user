from feeds.models import *
from .serializers import *
from django.http import JsonResponse
from rest_framework.response import Response
from django.core.paginator import Paginator
import json


def feed_as_object(data, feed_data_len, page):
    x = 0

    feeds_id = get_feeds_id()
    feeds_payload = []
    if x <= len(feeds_id):
        for id in feeds_id:
            user_comments = comments_payload(_feed=id)
            user_likes = likes_payload(_feed=id)
            feed = Feeds.objects.get(id=id)
            payload_result = {
                "feed_id": id,
                "user_id": feed.user_id.id,
                "user_name": feed.user_name,
                "content": feed.content,
                "created_at": feed.created_at,
                "update_at": feed.update_at,
                "comments": user_comments,
                "likes": user_likes,
            }
            feeds_payload.append(payload_result)
            x += 1

        # paginate feed-object
        result = []
        paginate_by = 10
        paginator = Paginator(feeds_payload, paginate_by)
        paginated_feed = paginator.get_page(page)
        for i in paginated_feed:
            result.append(i)
        return result


def get_feeds_id():
    results = []
    feeds_ids = Feeds.objects.all().values('id')
    for i in feeds_ids:
        results.append(i['id'])
    return results


def comments_payload(_feed):
    comments_payload = []
    comments = Comments.objects.filter(feed_id=_feed)
    for i in comments:
        user_comment_payload = {
            "comment_id": i.id,
            "user_id": i.user_id.id,
            "user_name": i.user_name,
            "content": i.content,
            "created_at": i.created_at,
            "update_at": i.update_at,
        }
        comments_payload.append(user_comment_payload)
    # print(json.dumps(comments_payload, indent=4))
    return comments_payload


def likes_payload(_feed):
    likes_payload = []
    likes = Likes.objects.filter(feeds__pk=_feed)
    for i in likes:
        user_likes_payload = {
            "like_id": i.id,
            "user_id": i.user_id.id,
            "user_name": i.user_name,
        }
        likes_payload.append(user_likes_payload)
    # print(json.dumps(likes_payload, indent=4))
    return likes_payload


def like_feed(id, user_id):
    like = Likes.objects.filter(user_id=user_id).first()
    like.feeds.add(id)
    FeedObject.add_like(u_id=user_id, f_id=id)

    serializer = LikesSerializer(
        Feeds.objects.get(id=id).user.all(), many=True)

    return serializer


def unlike_feed(id, user_id):
    like = Likes.objects.all().filter(user_id=user_id).first()
    like.feeds.remove(id)
    FeedObject.remove_like(u_id=user_id, f_id=id)

    x = Likes.objects.filter(user_id=user_id).first().feeds.all().exists()
    if not x:
        Likes.objects.filter(user_id=user_id).delete()
        serializer = ''

    feed = Feeds.objects.get(id=id).user.filter(feeds__pk=id)
    serializer = LikesSerializer(feed, many=True)
    return serializer
