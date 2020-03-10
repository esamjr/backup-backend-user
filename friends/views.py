from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Friends
from registrations.models import Register
from .serializers import FriendsSerializer
from registrations.serializers import RegisterSerializer

# watcher!
@api_view(['GET', 'POST'])
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

# get friend list of the designated user
@api_view(['GET'])
def friend_list(request, id):
    try:
        response = None
        # token = request.META.get('HTTP_AUTHORIZATION')
        user = Friends.objects.all().filter(user_id=id).first()
        # user = Friends.objects.all().filter(user_id=id)
        if user is None:

            response = {
                'api_status': status.HTTP_404_NOT_FOUND,
                'api_message': 'Friend list Tidak Ada'
            }

            return JsonResponse(response)
        else:
            _friends = user.friend_list.values()

            result = []
            for i in _friends:
                payload = {
                    'id': i['id'],
                    'email': i['email'],
                    'full_name': i['full_name'],
                    'verfied': i['verfied'],
                    'url_photo': i['url_photo']
                }

                response = {
                    'api_status': status.HTTP_200_OK,
                    'api_message': 'Friend list berhasil',
                    'data': result
                }

                result.append(payload)
            return JsonResponse(response, safe=False)
    except Exception as ex:
        response = {
            'error': str(ex),
            'status': ex.args
        }
        return JsonResponse(response)


# get friend suggestion of the designated user
@api_view(['GET'])
def friendsuggestion(request, id):
    try:
        if (request.method == 'GET'):
            user = Friends.objects.all().filter(user_id=id).first()
            exclude_all = [int(id)]
            exclude_friend = list(user.friend_list.all().values_list('id', flat=True).order_by('id'))
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

    except Exception as ex:
        response = {
            'error': str(ex),
            'status': ex.args
        }
        return JsonResponse(response)

# search base on name
@api_view(['GET'])
def search(request, id, name):
    try:
        if (request.method == 'GET'):
            user = Friends.objects.all().filter(user_id=id).first()
            exclude_all = [int(id)]
            exclude_friend = list(user.friend_list.all().values_list('id', flat=True).order_by('id'))
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

    except Exception as ex:
        response = {
            'error': str(ex),
            'status': ex.args
        }
        return JsonResponse(response)
        
# get friend request of the designated user
@api_view(['GET'])
def friend_request(request, id):
    try:
        response = None
        user = Friends.objects.all().filter(user_id=id).first()
        if user is None:
            response = {
                'api_status': status.HTTP_404_NOT_FOUND,
                'api_messages': 'Friend request tidak ada'
            }
            return JsonResponse(response)
        else:
            _friends = user.friend_request.values()

            result = []
            for i in _friends:
                payload = {
                    'id': i['id'],
                    'email': i['email'],
                    'full_name': i['full_name'],
                    'verfied': i['verfied'],
                    'url_photo': i['url_photo']
                }

                response = {
                    'api_status': status.HTTP_200_OK,
                    'api_message': 'Friend request berhasil',
                    'data': result
                }

                result.append(payload) 
            return JsonResponse(response, safe=False)

    except Exception as ex:
        response = {
            'error': str(ex),
            'status': ex.args
        }

        return JsonResponse(response)

@api_view(['POST'])
def cancel_friend_request(request, user_id):
    try:
        if (request.method == 'POST'):
            friend_request = get_object_or_404(request.user.friend_request, user_id=user_id)
            friend_request.cancel()

        return JsonResponse({'status':'cancel friend request'}, status=status.HTTP_200_OK)

     except Exception as ex:
        response = {
            'error': str(ex),
            'status': ex.args
        }
        return JsonResponse(response)
    
 # request for a new friend
@api_view(['PUT'])
def add_friend(request, user_id, friend_id):
    try:
        if (request.method == 'PUT'):
            user = Friends.objects.all().filter(user_id=user_id).first()
            user_friend = Friends.objects.all().filter(user_id=friend_id).first()
            user.waiting_for_response.add(Register.objects.get(id=friend_id))
            user_friend.friend_request.add(Register.objects.get(id=user_id))
            return Response({'status': user.user_name + ' Send friend request to ' + user_friend.user_name + ', waiting for response now..'}, status=status.HTTP_200_OK)
        else:
            if Friends.objects.filter(user_id=user_id).exists():
                return Response({'status': user_friend.user_name + ', Friend Already Exists'}, status=status.HTTP_200_OK)
    
    except Exception as ex:
        response = {
            'error': str(ex),
            'status': ex.args
        }

        return JsonResponse(response)
 # ignore friend request
@api_view(['PUT'])
def ignore_friend(request, user_id, friend_id):
    try:
        if (request.method == 'PUT'):
            user = Friends.objects.all().filter(user_id=user_id).first()
            user_friend = Friends.objects.all().filter(user_id=friend_id).first()
            user.friend_request.remove(friend_id)
            user_friend.waiting_for_response.remove(user_id)
            return Response({'status': user.user_name + ' ignore ' + user_friend.user_name + ' friend request'}, status=status.HTTP_200_OK)
    
    except Exception as ex:
        response = {
            'error': str(ex),
            'status': ex.args
        }
        return JsonResponse(response)
# accept friend request
@api_view(['PUT'])
def accept_friend(request, user_id, friend_id):
    try:
        if (request.method == 'PUT'):
            user = Friends.objects.all().filter(user_id=user_id).first()
            user.friend_request.remove(friend_id)
            user.friend_list.add(friend_id)
            user_friend = Friends.objects.all().filter(user_id=friend_id).first()
            user_friend.friend_list.add(user_id)
            user_friend.waiting_for_response.remove(user_id)
            return Response({'status': user.user_name + ' accept ' + user_friend.user_name + ' friend request'}, status=status.HTTP_200_OK)
    
    except Exception as ex:
        response = {
            'error': str(ex),
            'status': ex.args
        }

        return JsonResponse(response)
# unfriend
@api_view(['PUT'])
def unfriend(request, user_id, friend_id):
    try:
        if (request.method == 'PUT'):
            user = Friends.objects.all().filter(user_id=user_id).first()
            user.friend_list.remove(friend_id)
            user_friend = Friends.objects.all().filter(user_id=friend_id).first()
            user_friend.friend_list.remove(user_id)
            return Response({'status': user.user_name + ' unfriend ' + user_friend.user_name}, status=status.HTTP_200_OK)
    
    except Exception as ex:
        response = {
            'error': str(ex),
            'status': ex.args
        }
        return JsonResponse(response)