from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Feeds, Comments, Likes, FeedObject
from .services import feed_as_object, like_feed, unlike_feed
from .serializers import (
    FeedsSerializer,
    FeedObjectSerializer,
    CommentsSerializer,
    LikesSerializer)


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
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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

    # DEFAULT
    :request feed-id *FK:
    :request comments *MtMf:
    :request likes *MtMf:
    """
    try:
        if request.method == 'GET':
            serializer = FeedObjectSerializer(
                FeedObject.objects.all(), many=True)
            feeds_ = len(Feeds.objects.all())

            response = {
                'api_status': status.HTTP_200_OK,
                'api_message': 'viewing feeds-object',
                'data': feed_as_object(serializer.data, feed_data_len=feeds_)
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
        id = int(request.query_params['id'])
        if request.method == 'PUT':
            feed = Feeds.objects.filter(
                id=id, user_name=request.data['user_name']).first()

            serializer = FeedsSerializer(feed, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    'api_status': status.HTTP_200_OK,
                    'api_message': 'feed updated',
                    'data': serializer.data
                }
                return JsonResponse(response)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            Feeds.objects.filter(id=id).delete()
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
        if request.method == 'GET':
            id = int(request.query_params['feed_id'])

            feed = Feeds.objects.get(id=id)
            feed_likes = Likes.objects.filter(feeds__pk=id)
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
        if request.method == 'PUT':
            id = int(request.query_params['id'])
            user_id = int(request.query_params['user_id'])

            if Likes.objects.filter(user_id=user_id):
                serializer = like_feed(id=id, user_id=user_id)
            else:
                serializer = Likes.instantiate_like_obj(id=id, user_id=user_id)

            response = {
                'api_status': status.HTTP_200_OK,
                'api_message': f'you like post {id}',
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
        if request.method == 'PUT':
            id = int(request.query_params['id'])
            user_id = int(request.query_params['user_id'])

            serializer = unlike_feed(id=id, user_id=user_id)
            response = {
                'api_status': status.HTTP_200_OK,
                'api_message': f'you unlike post {id}',
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
        if request.method == 'GET':
            id = int(request.query_params['feed_id'])

            feed = Feeds.objects.get(id=id)
            comments = Comments.objects.filter(feed_id__pk=id)
            serializer = CommentsSerializer(comments, many=True)
            response = {
                'api_status': status.HTTP_200_OK,
                'api_message': f'comment counts',
                'data': [
                    {
                        "feed_id": feed.id,
                        "feed_content": feed.content,
                        "comments_count": len(serializer.data)
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
        id = request.query_params['id']

        if request.method == 'PUT':
            comment = Comments.objects.get(id=id)
            serializer = CommentsSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    'api_status': status.HTTP_200_OK,
                    'api_message': 'comment edited',
                    'data': serializer.data
                }
                return JsonResponse(response)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            Comments.objects.filter(id=id).delete()
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
