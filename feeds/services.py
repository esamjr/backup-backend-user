from feeds.models import *
from .serializers import *
from django.http import JsonResponse
from rest_framework.response import Response
import json


def feed_as_object(data, feed_data_len):
    if data and feed_data_len:
        feeds_id = get_feeds_id()

    x = 0
    feeds_payload = []
    if x <= len(feeds_id):
        for id in feeds_id:
            user_comments = comments_payload(_feed=id)
            user_likes = likes_payload(_feed=id)
            payload_result = {
                "feed_id": id,
                "user_id": Feeds.objects.get(id=id).user_id.id,
                "user_name": Feeds.objects.get(id=id).user_name,
                "content": Feeds.objects.get(id=id).content,
                "comments": user_comments,
                "likes": user_likes,
            }
            feeds_payload.append(payload_result)
            x += 1
        return feeds_payload


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
            "id": i.id,
            "user_id": i.user_id.id,
            "user_name": i.user_name,
            "content": i.content,
        }
        comments_payload.append(user_comment_payload)
    # print(json.dumps(comments_payload, indent=4))
    return comments_payload


def likes_payload(_feed):
    likes_payload = []
    likes = Likes.objects.filter(feeds__pk=_feed)
    for i in likes:
        user_likes_payload = {
            "id": i.id,
            "user_id": i.user_id.id,
            "user_name": i.user_name,
        }
        likes_payload.append(user_likes_payload)
    # print(json.dumps(likes_payload, indent=4))
    return likes_payload


def like_feed(id, user_id):
    like = Likes.objects.filter(user_id=user_id).first()
    like.feeds.add(id)
    FeedObject.like_feed(u_id=user_id, f_id=id)

    serializer = LikesSerializer(
        Feeds.objects.get(id=id).user.all(), many=True)
    response = {
        'api_status': status.HTTP_200_OK,
        'api_message': f'you like post {id}',
        'data': serializer.data
    }
    return JsonResponse(response)
