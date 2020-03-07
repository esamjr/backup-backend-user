from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import FeedsObj, Comments, Likes, Feed
from .serializers import (
    FeedsObjSerializer,
    FeedSerializer,
    CommentsSerializer,
    LikesSerializer)
import json


@api_view(['GET', 'POST'])
def get_post_feeds(request):
    """
    API Endpoint that allows user to view-feeds or create-feed

    :param request:
        :request user-id:
        :request user-name:
        :request content:
    """
    try:
        if request.method == 'GET':
            feeds = FeedsObj.objects.all()
            serializer = FeedsObjSerializer(feeds, many=True)
            response = {
                'api_status': status.HTTP_200_OK,
                'api_message': 'Success viewing feeds!',
                'data': serializer.data
            }
            return JsonResponse(response)

        if request.method == 'POST':
            serializer = FeedsObjSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                # Bug, does not support list :but, dict
                Feed.instantiate_feeds()
                # end-bug
                response = {
                    'api_status': status.HTTP_201_CREATED,
                    'api_message': 'Success create feed!',
                    'data': serializer.data
                }
                return JsonResponse(response)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        response = {
            'api_error': str(ex),
            'api_message': ex.args
        }
        return JsonResponse(response)


@api_view(['PUT', 'DELETE'])
def put_delete_feed(request, feed_id):
    """
    API Endpoint that allows user to edit-feed or delete-feed

    :param request:
        :request user-id:
        :request user-name:
        :request content:
    :param feed-id:
    """
    try:
        if request.method == 'PUT':
            feed = FeedsObj.objects.get(id=feed_id)
            serializer = FeedsObjSerializer(feed, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    'api_status': status.HTTP_200_OK,
                    'api_message': 'Success update feed!',
                    'data': serializer.data
                }
                return JsonResponse(response)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.method == "DELETE":
            feed = FeedsObj.objects.filter(id=feed_id)
            feed.delete()
            response = {
                'api_status': status.HTTP_204_NO_CONTENT,
                'api_message': 'Success delete feed!',
                'data': None
            }
            return JsonResponse(response)
    except Exception as ex:
        response = {
            'api_error': str(ex),
            'api_message': ex.args
        }
        return JsonResponse(response)


@api_view(['POST'])
def create_user_like(request):
    try:
        serializer = LikesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'api_status': status.HTTP_201_CREATED,
                'api_message': 'Success create user-like!',
                'data': serializer.data
            }
            return JsonResponse(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        response = {
            'api_error': str(ex),
            'api_message': ex.args
        }
        return JsonResponse(response)


@api_view(['GET'])
def show_likes(request):
    """
    API Endpoint that allows user to view user-likes
    """
    try:
        if request.method == 'GET':
            likes = Likes.objects.all()
            serializer = LikesSerializer(likes, many=True)
            response = {
                'api_status': status.HTTP_200_OK,
                'api_message': 'Success viewing likes!',
                'data': serializer.data
            }
            return JsonResponse(response)
    except Exception as ex:
        response = {
            'api_error': str(ex),
            'api_message': ex.args
        }
        return JsonResponse(response)


@api_view(['GET'])
def specific_user_like(request, user_id):
    """
    API Endpoint that allows user to view specific-users-feeds-likes

    :param request:
    :param user-id:
    """
    try:
        if request.method == 'GET':
            user = Likes.objects.get(user_id=user_id)
            serializer = LikesSerializer(user)
            response = {
                'api_status': status.HTTP_200_OK,
                'api_message': 'Success viewing user feed likes!',
                'data': serializer.data
            }
            return JsonResponse(response)
    except Exception as ex:
        response = {
            'api_error': str(ex),
            'api_message': ex.args
        }
        return JsonResponse(response)


@api_view(['GET'])
def liked_feed(request, feed_id):
    """
    API Endpoint that allows user to view specific-feed-likes-count

    :param request:
    :param feed-id:
    """
    try:
        if request.method == 'GET':
            likes = FeedsObj.objects.get(id=feed_id).user.all()
            serializer = LikesSerializer(likes, many=True)
            response = {
                'api_status': status.HTTP_200_OK,
                'api_message': 'Success viewing feed likes count',
                'data': serializer.data
            }
            return JsonResponse(response)
    except Exception as ex:
        response = {
            'api_error': str(ex),
            'api_message': ex.args
        }
        return JsonResponse(response)


@api_view(['PUT'])
def like(request, user_id, feed_id):
    """
    API Endpoint that allows user to like-feed

    :param request:
    :param user-id:
    :param feed-id:
    """
    try:
        user = Likes.objects.all().filter(user_id=user_id).first()
        if request.method == 'PUT':
            user.feeds.add(feed_id)
            likes = FeedsObj.objects.get(id=feed_id).user.all()
            serializer = LikesSerializer(likes, many=True)
            response = {
                'api_status': status.HTTP_200_OK,
                'api_message': str(user.user_name)+' like post '+str(feed_id),
                'data': serializer.data
            }
            return JsonResponse(response)
    except Exception as ex:
        response = {
            'api_error': str(ex),
            'api_message': ex.args
        }
        return JsonResponse(response)


@api_view(['PUT'])
def unlike(request, user_id, feed_id):
    """
    API Endpoint that allows user to unlike-feed

    :param request:
    :param user-id:
    :param feed-id:
    """
    try:
        user = Likes.objects.all().filter(user_id=user_id).first()
        if request.method == 'PUT':
            user.feeds.remove(feed_id)
            likes = FeedsObj.objects.get(id=feed_id).user.all()
            serializer = LikesSerializer(likes, many=True)
            response = {
                'api_status': status.HTTP_200_OK,
                'api_message': str(user.user_name)+' unlike post '+str(feed_id),
                'data': serializer.data
            }
            return JsonResponse(response)
    except Exception as ex:
        response = {
            'api_error': str(ex),
            'api_message': ex.args
        }
        return JsonResponse(response)


@api_view(['GET', 'POST'])
def get_post_comments(request):
    """
    API Endpoint that allows user to view-comments and create-comment

    :param request:
        :request user-id:
        :request feeds-id:
        :request user-name:
        :request content:
    """
    try:
        if request.method == 'GET':
            comments = Comments.objects.all()
            serializer = CommentsSerializer(comments, many=True)
            response = {
                'api_status': status.HTTP_200_OK,
                'api_message': 'Success viewing comments!',
                'data': serializer.data
            }
            return JsonResponse(response)

        if request.method == 'POST':
            serializer = CommentsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                # Bug, does not support dict nor list
                Feed.instantiate_comment(request.data['feeds_id'])
                # end-bug
                response = {
                    'api_status': status.HTTP_201_CREATED,
                    'api_message': 'Success creating comments!',
                    'data': serializer.data
                }
                return JsonResponse(response)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        response = {
            'api_error': str(ex),
            'api_message': ex.args
        }
        return JsonResponse(response)


@api_view(['GET'])
def specific_feed_comment(request, feed_id):
    """
    API Endpoint that allows user to view-specific-comment

    :param request:
    :param feeds-id:
    """
    try:
        # Bug, feeds doesn't show the comment-object, just show comment-id.
        if request.method == 'GET':
            feed = Feed.objects.filter(feed_id=feed_id)
            serializer = FeedSerializer(feed, many=True)
            response = {
                'api_status': status.HTTP_200_OK,
                'api_message': 'Success viewing specific feed comments!',
                'data': serializer.data
            }
            return JsonResponse(response)
    except Exception as ex:
        response = {
            'api_error': str(ex),
            'api_message': ex.args
        }
        return JsonResponse(response)


@api_view(['GET'])
def comments_count(request, feed_id):
    """
    API Endpoint that allows user to view-feed-comments-count

    :param request:
    :param feeds-id:
    """
    try:
        if (request.method == 'GET'):
            comments = Comments.objects.filter(feeds_id__id=feed_id)
            serializer = CommentsSerializer(comments, many=True)
            response = {
                'api_status': status.HTTP_200_OK,
                'api_message': 'Success viewing comments-count {}'.format(len(serializer.data)),
                'data': serializer.data
            }
            return JsonResponse(response)
    except Exception as ex:
        response = {
            'api_error': str(ex),
            'api_message': ex.args
        }
        return JsonResponse(response)


@api_view(['PUT', 'DELETE'])
def edit_delete_comment(request, comment_id):
    """
    API Endpoint that allows user to delete-comment

    :param request:
        :request user-id:
        :request user-name:
        :request content:
    :param comment-id:
    """
    try:
        if request.method == 'PUT':
            comment = Comments.objects.get(id=comment_id)
            serializer = CommentsSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    'api_status': status.HTTP_200_OK,
                    'api_message': 'Success edit comment',
                    'data': serializer.data
                }
                return JsonResponse(response)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.method == "DELETE":
            Comments.objects.filter(id=comment_id).delete()
            response = {
                'api_status': status.HTTP_204_NO_CONTENT,
                'api_message': 'Success delete comment',
                'data': None
            }
            return JsonResponse(response)
    except Exception as ex:
        response = {
            'api_error': str(ex),
            'api_message': ex.args
        }
        return JsonResponse(response)
