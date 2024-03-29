from django.http import JsonResponse
import json

from .models import Feeds, Comments, Likes
from .services import feed_as_object, like_feed, unlike_feed
from .signals import *
from .serializers import (
    FeedsSerializer,
    CommentsSerializer,
    LikesSerializer)

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(['GET', 'POST'])
def get_post_feed(request):
    """
    API Endpoint that allows user to view-feeds or create-feed

    # POST
    ::param request:
    :request user-id:
    :request user-name:
    :request content:
    """
    try:
        if request.method == 'GET':
            serializer = FeedsSerializer(Feeds.objects.all(), many=True)
            response = {
                'api_status': status.HTTP_200_OK,
                'api_message': 'viewing feeds',
                'data': serializer.data
            }
            return JsonResponse(response)

        if request.method == 'POST':
            serializer = FeedsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    'api_status': status.HTTP_201_CREATED,
                    'api_message': 'feed created',
                    'data': serializer.data
                }
                return JsonResponse(response)
    except Exception as ex:
        response = {
            'api_error': status.HTTP_400_BAD_REQUEST,
            'api_message': str(ex.args)
        }
        return JsonResponse(response)


@api_view(['GET'])
def feed_object(request):
    """
    API Endpoint that allows user to view feeds-in-object
    """
    try:
        page = request.GET.get('page')
        if request.method == 'GET':
            paginated_feed, page_len = feed_as_object(page=page)
            response = {
                'api_status': status.HTTP_200_OK,
                'api_message': 'viewing feeds-object',
                'page_length': page_len,
                'data': paginated_feed
            }
            return JsonResponse(response)
    except Exception as ex:
        response = {
            'api_error': status.HTTP_400_BAD_REQUEST,
            'api_message': str(ex.args)
        }
        return JsonResponse(response)


@api_view(['PUT', 'DELETE'])
def put_delete_feed(request):
    """
    API Endpoint that allows user to edit-feed or delete-feed

    # PUT
    ::param request:
    :request user-id:
    :request user-name:
    :request content:

    # DELETE
    ::param id *feed-id:
    """
    try:
        _id = int(request.query_params['id'])
        _username = str(request.data['user_name'])
        if request.method == 'PUT':
            feed = Feeds.objects.filter(
                id=_id, user_name=_username).first()
            serializer = FeedsSerializer(feed, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    'api_status': status.HTTP_200_OK,
                    'api_message': 'feed updated',
                    'data': serializer.data
                }
                return JsonResponse(response)

        if request.method == 'DELETE':
            Feeds.objects.filter(id=_id).delete()
            response = {
                'api_status': status.HTTP_204_NO_CONTENT,
                'api_message': 'feed deleted',
                'data': None
            }
            return JsonResponse(response)
    except Exception as ex:
        response = {
            'api_error': status.HTTP_400_BAD_REQUEST,
            'api_message': str(ex.args)
        }
        return JsonResponse(response)


@api_view(['GET'])
def likes(request):
    """
    API Endpoint that allows user to view likes
    """
    try:
        if request.method == 'GET':
            serializer = LikesSerializer(Likes.objects.all(), many=True)
            response = {
                'api_status': status.HTTP_200_OK,
                'api_message': 'viewing likes',
                'data': serializer.data
            }
            return JsonResponse(response)
    except Exception as ex:
        response = {
            'api_error': status.HTTP_400_BAD_REQUEST,
            'api_message': str(ex.args)
        }
        return JsonResponse(response)


@api_view(['GET'])
def feed_likes_count(request):
    """
    API Endpoint that allows user to view specific-feed-likes-count

    # GET
    :param feed-id:
    """
    try:
        _id = int(request.query_params['feed_id'])
        if request.method == 'GET':
            feed = Feeds.objects.get(id=_id)
            feed_likes = Likes.objects.filter(feeds__pk=_id)
            serializer = LikesSerializer(feed_likes, many=True)

            response = {
                'api_status': status.HTTP_200_OK,
                'api_message': 'viewing feed likes count',
                'data': [
                    {
                        "feed_id": feed.id,
                        "feed_content": feed.content,
                        "likes_count": len(serializer.data)
                    }
                ]
            }
            return JsonResponse(response)
    except Exception as ex:
        response = {
            'api_error': status.HTTP_400_BAD_REQUEST,
            'api_message': str(ex.args)
        }
        return JsonResponse(response)


@api_view(['PUT'])
def like(request):
    """
    API Endpoint that allows user to like-feed

    # PUT
    :param id *feed-id:
    :param user-id:
    """
    try:
        _id = int(request.query_params['id'])
        _userid = int(request.query_params['user_id'])
        if request.method == 'PUT':
            if Likes.objects.filter(user_id=_userid):
                serializer = like_feed(id=_id, user_id=_userid)
            else:
                serializer = Likes.instantiate_like_obj(
                    id=_id, user_id=_userid)

            response = {
                'api_status': status.HTTP_200_OK,
                'api_message': f'you like post {_id}',
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
def unlike(request):
    """
    API Endpoint that allows user to unlike-feed

    # PUT
    :param id *user-id:
    :param feed-id:
    """
    try:
        _id = int(request.query_params['id'])
        _userid = int(request.query_params['user_id'])
        if request.method == 'PUT':
            serializer = unlike_feed(id=_id, user_id=_userid)

            response = {
                'api_status': status.HTTP_200_OK,
                'api_message': f'you unlike post {_id}',
                'data': f'feed likes count : {len(serializer.data)}'
            }
            return JsonResponse(response)
    except Exception as ex:
        response = {
            'api_error': str(ex),
            'api_message': ex.args
        }
        return JsonResponse(response)


@api_view(['GET', 'POST'])
def get_post_comment(request):
    """
    API Endpoint that allows user to view-comments and create-comment

    # POST
    ::param request:
    :request user-id:
    :request feed-id:
    :request user-name:
    :request content:
    """
    try:
        if request.method == 'GET':
            serializer = CommentsSerializer(Comments.objects.all(), many=True)
            response = {
                'api_status': status.HTTP_200_OK,
                'api_message': 'viewing comments',
                'data': serializer.data
            }
            return JsonResponse(response)

        if request.method == 'POST':
            serializer = CommentsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    'api_status': status.HTTP_201_CREATED,
                    'api_message': 'comment created',
                    'data': serializer.data
                }
                return JsonResponse(response)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        response = {
            'api_error': status.HTTP_400_BAD_REQUEST,
            'api_message': str(ex.args)
        }
        return JsonResponse(response)


@api_view(['GET'])
def comment_feed_count(request):
    """
    API Endpoint that allows user to view feeds-comments count

    # GET
    :param feed-id:
    """
    try:
        _id = int(request.query_params['feed_id'])
        if request.method == 'GET':
            feed = Feeds.objects.get(id=_id)
            comments = Comments.objects.filter(feed_id__pk=_id)
            serializer = CommentsSerializer(comments, many=True)

            response = {
                'api_status': status.HTTP_200_OK,
                'api_message': f'comment counts',
                'data': len(serializer.data)
            }
            return JsonResponse(response)
    except Exception as ex:
        response = {
            'api_error': status.HTTP_400_BAD_REQUEST,
            'api_message': str(ex.args)
        }
        return JsonResponse(response)


@api_view(['PUT', 'DELETE'])
def put_delete_comment(request):
    """
    API Endpoint that allows user to edit and delete comment

    # PUT
    ::param request:
    :request user-id:
    :request user-name:
    :request content:

    # DELETE
    ::param comment-id:
    """
    try:
        _id = int(request.query_params['id'])
        if request.method == 'PUT':
            comment = Comments.objects.get(id=_id)
            serializer = CommentsSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    'api_status': status.HTTP_200_OK,
                    'api_message': 'comment edited',
                    'data': serializer.data
                }
                return JsonResponse(response)

        if request.method == 'DELETE':
            Comments.objects.filter(id=_id).delete()
            response = {
                'api_status': status.HTTP_204_NO_CONTENT,
                'api_message': 'comment deleted',
                'data': None
            }
            return JsonResponse(response)
    except Exception as ex:
        response = {
            'api_error': str(ex),
            'api_message': ex.args
        }
        return JsonResponse(response)
