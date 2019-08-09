from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from django.shortcuts import render
from .models import FeedsObj, LikesNComments, UserLike
from .serializers import FeedsObjSerializer, LikesNCommentsSerializer, UserLikeSerializer
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
        return Response({'status': 'bad request anjing'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
def get_post_delete_likesncomments(request):
    if request.method == 'GET':
        beacon = LikesNComments.objects.all()
        serializer = LikesNCommentsSerializer(beacon, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = LikesNCommentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        beacon = LikesNComments.objects.all()
        beacon.delete()
        return Response({'status': 'Delete succesful!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST', 'GET'])
def get_post_specific_likesncomments(request, pk):
    try:
        feed = FeedsObj.objects.get(id=pk)
    except:
        return Response({'status': 'feeds tidak ketemu :('}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        tmp_data = request.data.copy()
        tmp_data['feedsobj'] = feed.id
        print(tmp_data)
        serializer = LikesNCommentsSerializer(data=tmp_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        beacon = LikesNComments.objects.filter(feedsobj__pk=feed.id)
        serializer = LikesNCommentsSerializer(beacon, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def put_add_likes(request, user_pk, feedsobj_pk):
    beacon = UserLike.objects.all().filter(user_id=user_pk)
    beacon = beacon.first()
    print(beacon)
    beacon.feedsobjs.add(FeedsObj.objects.get(id=feedsobj_pk))
    return Response({'status': 'status oke!'}, status=status.HTTP_200_OK)

@api_view(['PUT'])
def put_delete_likes(request, user_pk, feedsobj_pk):
    beacon = UserLike.objects.all().filter(user_id=user_pk)
    beacon = beacon.first()
    beacon.feedsobjs.remove(feedsobj_pk)
    return Response({'status': 'status oke!'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def post_likes(request):
    if request.method == 'POST':
        serializer = UserLikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def get_likes(request):
    beacon = UserLike.objects.all()
    serializer = UserLikeSerializer(beacon, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_specific_likes(request, pk):
    beacon = UserLike.objects.all().filter(user_id=pk)
    beacon = beacon.first()
    serializer = UserLikeSerializer(beacon)
    return Response(serializer.data, status=status.HTTP_200_OK)