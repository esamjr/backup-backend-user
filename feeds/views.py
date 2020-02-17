from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from django.shortcuts import render
from .models import FeedsObj, Comments, Likes
from .serializers import FeedsObjSerializer, CommentsSerializer, LikesSerializer
# Create your views here.


@api_view(['GET', 'POST', 'DELETE'])
def get_post_delete_feeds(request):
    if request.method == 'GET':
        beacon = FeedsObj.objects.all()
        serializer = FeedsObjSerializer(beacon, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = FeedsObjSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        beacon = FeedsObj.objects.all()
        beacon.delete()
        return Response({'status': 'Delete succesful!'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
def put_feeds(request, pk):
    if request.method == 'PUT':
        beacon = FeedsObj.objects.get(id=pk)
        serializer = FeedsObjSerializer(beacon, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'status': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)

# likes watcher
@api_view(['GET'])
def likes(request):
    if (request.method == 'GET'):
        likes = Likes.objects.all()
        serializer = LikesSerializer(likes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# likes specific watcher
@api_view(['GET'])
def likes_specific(request, pk):
    if (request.method == 'GET'):
        user = Likes.objects.all().filter(user=pk).first()
        serializer = LikesSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

# create new likes object
@api_view(['POST'])
def likes_create(request):
    if request.method == 'POST':
        serializer = LikesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# add new feeds you like
@api_view(['PUT'])
def likes_like(request, user_pk, feeds_pk):
    if (request.method == 'PUT'):
        user = Likes.objects.all().filter(user=user_pk).first()
        user.feeds.add(feeds_pk)
        return Response({'status': user.name + ' like post ' + feeds_pk}, status=status.HTTP_200_OK)

# undo feeds you like
@api_view(['PUT'])
def likes_unlike(request, user_pk, feeds_pk):
    if (request.method == 'PUT'):
        user = Likes.objects.all().filter(user=user_pk).first()
        user.feeds.remove(feeds_pk)
        return Response({'status': user.name + ' unlike post ' + feeds_pk}, status=status.HTTP_200_OK)

# see how many likes in feeds
@api_view(['GET'])
def likes_count(request, feeds_pk):
    if (request.method == 'GET'):
        likes = FeedsObj.objects.get(id=feeds_pk).user.all()
        serializer = LikesSerializer(likes, many=True)
        return Response({'likes_count': len(serializer.data)}, status=status.HTTP_200_OK)

# comments watcher
@api_view(['GET', 'POST', 'DELETE'])
def comments(request):
    if (request.method == 'GET'):
        comments = Comments.objects.all()
        serializer = CommentsSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif (request.method == 'POST'):
        serializer = CommentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif (request.method == 'DELETE'):
        comments = Comments.objects.all()
        comments.delete()
        return Response({'status': 'Delete all comments!'}, status=status.HTTP_204_NO_CONTENT)

# comments specific watcher
@api_view(['POST', 'GET'])
def comments_specific(request, pk):
    try:
        feeds = FeedsObj.objects.get(id=pk)
    except:
        return Response({'status': 'feeds tidak ketemu :('}, status=status.HTTP_404_NOT_FOUND)
    if (request.method == 'GET'):
        comments = Comments.objects.filter(feeds__pk=pk)
        serializer = CommentsSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# see how many comments in feeds
@api_view(['GET'])
def comments_count(request, feeds_pk):
    if (request.method == 'GET'):
        comments = comments = Comments.objects.filter(feeds__pk=feeds_pk)
        serializer = CommentsSerializer(comments, many=True)
        return Response({'comments_count':len(serializer.data)}, status=status.HTTP_200_OK)
