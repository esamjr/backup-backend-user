from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from django.shortcuts import render
from django.http import JsonResponse
from .models import Friends
from registrations.models import Register, Domoo
from .serializers import FriendsSerializer
from registrations.serializers import RegisterSerializer
 
# watcher!
@api_view(['GET', 'POST', 'DELETE'])
def watcher(request):
    if request.method == 'GET':
        users = Friends.objects.all()
        serializer = FriendsSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = FriendsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'DELETE':
        users = Friends.objects.all()
        users.delete()
        return Response({'status': 'deleted all friends connection'}, status=status.HTTP_204_NO_CONTENT)

# get friend list of the designated user
@api_view(['GET'])
def friendlist(request, pk):
    # token = request.META.get('HTTP_AUTHORIZATION')
    user = Friends.objects.all().filter(user_id=pk).first()
    if (user is None):
        
        serializer = FriendsSerializer(data=request.data)
        
        return JsonResponse({'status': 'empty'})
    else :
        friendlist = list(user.registers.values())
        return JsonResponse(friendlist, safe=False)

# get friend suggestion of the designated user
@api_view(['GET'])
def friendsuggestion(request, pk):
    if (request.method == 'GET'):
        user = Friends.objects.all().filter(user_id=pk).first()
        exclude_all = [int(pk)]
        exclude_friend = list(user.registers.all().values_list('id', flat=True).order_by('id'))
        exclude_friend_request = list(user.friend_request.all().values_list('id', flat=True).order_by('id'))
        exclude_waiting_for_response = list(user.waiting_for_response.all().values_list('id', flat=True).order_by('id'))
        for item in exclude_friend:
            exclude_all.append(int(item))
        for item in exclude_friend_request:
            exclude_all.append(int(item))
        for item in exclude_waiting_for_response:
            exclude_all.append(int(item))
        friend_suggestion = Register.objects.all().exclude(id__in=exclude_all)
        serializer = RegisterSerializer(friend_suggestion, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# search base on name
@api_view(['GET'])
def search(request, pk, name):
    if (request.method == 'GET'):
        user = Friends.objects.all().filter(user_id=pk).first()
        exclude_all = [int(pk)]
        exclude_friend = list(user.registers.all().values_list('id', flat=True).order_by('id'))
        exclude_friend_request = list(user.friend_request.all().values_list('id', flat=True).order_by('id'))
        exclude_waiting_for_response = list(user.waiting_for_response.all().values_list('id', flat=True).order_by('id'))
        for item in exclude_friend:
            exclude_all.append(int(item))
        for item in exclude_friend_request:
            exclude_all.append(int(item))
        for item in exclude_waiting_for_response:
            exclude_all.append(int(item))
        friend_suggestion = Register.objects.all().exclude(id__in=exclude_all)
        constrains = name.split("%")
        for constrain in constrains:
            search_result = friend_suggestion.filter(full_name__icontains=constrain)
        serializer = RegisterSerializer(search_result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# get friend request of the designated user 
@api_view(['GET'])
def friend_request(request, pk):
    if (request.method == 'GET'):
        user = Friends.objects.all().filter(user_id=pk).first()
        if (user == None):
            return JsonResponse({'status': 'empty'})
        else :
            friend_request = list(user.friend_request.values())
            return JsonResponse(friend_request, safe=False)

 # request for a new friend
@api_view(['PUT'])
def add_friend(request, user_pk, friend_pk):
    if (request.method == 'PUT'):
        user = Friends.objects.all().filter(user_id=user_pk).first()
        user_friend = Friends.objects.all().filter(user_id=friend_pk).first()
        user.waiting_for_response.add(Register.objects.get(id=friend_pk))
        user_friend.friend_request.add(Register.objects.get(id=user_pk))
        return Response({'status': user.user_name + ' Send friend request to ' + user_friend.user_name + ', waiting for response now..'}, status=status.HTTP_200_OK)

 # ignore friend request
@api_view(['PUT'])
def ignore_friend(request, user_pk, friend_pk):
    if (request.method == 'PUT'):
        user = Friends.objects.all().filter(user_id=user_pk).first()
        user_friend = Friends.objects.all().filter(user_id=friend_pk).first()
        user.friend_request.remove(friend_pk)
        user_friend.waiting_for_response.remove(user_pk)
        return Response({'status': user.user_name + ' ignore ' + user_friend.user_name + ' friend request'}, status=status.HTTP_200_OK)

# accept friend request
@api_view(['PUT'])
def accept_friend(request, user_pk, friend_pk):
    if (request.method == 'PUT'):
        user = Friends.objects.all().filter(user_id=user_pk).first()
        user.friend_request.remove(friend_pk)
        user.registers.add(friend_pk)
        user_friend = Friends.objects.all().filter(user_id=friend_pk).first()
        user_friend.registers.add(user_pk)
        user_friend.waiting_for_response.remove(user_pk)
        return Response({'status': user.user_name + ' accept ' + user_friend.user_name + ' friend request'}, status=status.HTTP_200_OK)

#unfriend
@api_view(['PUT'])
def unfriend(request, user_pk, friend_pk):
    if (request.method == 'PUT'):
        user = Friends.objects.all().filter(user_id=user_pk).first()
        user.registers.remove(friend_pk)
        user_friend = Friends.objects.all().filter(user_id=friend_pk).first()
        user_friend.registers.remove(user_pk)   
        return Response({'status': user.user_name + ' unfriend ' + user_friend.user_name}, status=status.HTTP_200_OK)