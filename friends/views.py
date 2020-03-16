from django.http import JsonResponse
from django.core.cache import cache
from django.core import serializers
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from registrations.models import Register
from registrations.serializers import RegisterSerializer, RegisterFriendsSerializers
from .models import Friends
from .serializers import FriendsSerializer

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@api_view(['GET', 'POST'])
@cache_page(CACHE_TTL)
def watcher(request):
    """
    API Endpoint that allows user to view-user-friend and post-user-friend
    """
    try:
        
        if request.method == 'GET':
            users = Friends.objects.all()
            # Check if Data exist in cache
            if 'users' in cache:
                users = cache.get('users')
                return Response(users, status=status.HTTP_200_OK)
            # Else add into cache them send to the response
            else:
                data = serializers.serialize('json', users)
                cache.set('users', data, timeout=CACHE_TTL)
                serializer = FriendsSerializer(users, many=True)
                response = {
                    'api_status': status.HTTP_200_OK,
                    'api_message': 'viewing user-friend-datas',
                    'data': serializer.data
                }
                return JsonResponse(response)


        if request.method == 'POST':
            serializer = FriendsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    'api_status': status.HTTP_201_CREATED,
                    'api_message': 'user-friend-data created',
                    'data': serializer.data
                }
                return JsonResponse(response)
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    except Exception as ex:
        response = {
            'api_error': status.HTTP_400_BAD_REQUEST,
            'api_message': str(ex.args)
        }
        return JsonResponse(response)

@api_view(['GET'])
@cache_page(CACHE_TTL)
def user_friends_list(request):
    """
    API Endpoint that allows user to specific user-friends-list
    """
    try:
        id = int(request.query_params['user_id'])
        if request.method == 'GET':
            # Check if Data exist in cache
            if 'friend_list' in cache:
                friend_list = cache.get('friend_list')
                response = {
                    'api_status':status.HTTP_200_OK,
                    'api_message': 'user-friend-list Loaded',
                    'data':friend_list
                }
                return JsonResponse(response)
            # Else add into cache them send to the response
            else:
                user = Friends.objects.all().filter(user_id=id).first()
                if user:
                    data = serializers.serialize('json', user.friend_list.only('id','email','full_name','verfied','url_photo'))
                    cache.set("friend_list", data, timeout=CACHE_TTL)
                    user_register = Register.objects.get(id=id)
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
                        result.append(payload)

                    paginator = Paginator(_friends, 12)
                    page = request.GET.get('page')
                    items = paginator.get_page(page)

                    response = {
                        'api_status': status.HTTP_200_OK,
                        'api_message': 'Friend list berhasil',
                        'items':items,
                        'data': {
                            'user_id': id,
                            'user_name': user_register.full_name,
                            'friends_list': result
                        }
                    }
                    return JsonResponse(response)

                else:
                    response = {
                        'api_status': status.HTTP_200_OK,
                        'api_message': 'User tidak ada',
                    }
                    return JsonResponse(response)
    except Exception as ex:
        response = {
            'error': status.HTTP_400_BAD_REQUEST,
            'status': ex.args
        }
        return JsonResponse(response)


@api_view(['GET'])
@cache_page(CACHE_TTL)
def friend_request(request):
    """
    API Endpoint that allows user to see list-friend-request
    """
    try:
        id = int(request.query_params['user_id'])
        if 'friend_request' in cache:
            friend_list = cache.get('friend_request')
            response = {
                'api_status':status.HTTP_200_OK,
                'api_message': 'user-friend-request Loaded',
                'data':friend_list
            }
            return JsonResponse(response)

        else:
            user = Friends.objects.all().filter(user_id=id).first()
            if request.method == 'GET':
                if user:
                    data = serializers.serialize('json', user.friend_request.only('id','email','full_name','verfied','url_photo'))
                    cache.set("friend_request", data, timeout=CACHE_TTL)
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
                        result.append(payload)
                    response = {
                        'api_status': status.HTTP_200_OK,
                        'api_message': 'Friend request berhasil',
                        'data': result
                    }
                    return JsonResponse(response, safe=False)
                else:
                    response = {
                        'api_status': status.HTTP_404_NOT_FOUND,
                        'api_messages': 'Friend request tidak ada'
                    }
                    return JsonResponse(response, safe=False)
    except Exception as ex:
        response = {
            'error': status.HTTP_400_BAD_REQUEST,
            'status': ex.args
        }
        return JsonResponse(response)


@api_view(['GET'])
@cache_page(CACHE_TTL)
def friend_request_list(request):
    """
    API Endpoint that allows user can see history-send-friend-request
    """
    try:
        id = int(request.query_params['user_id'])
        # Check if Data exist in cache
        if 'friend_request_list' in cache:
            friend_list = cache.get('friend_request')
            response = {
                'api_status':status.HTTP_200_OK,
                'api_message': 'friend-request-list Loaded',
                'data':friend_list
            }
            return JsonResponse(response)
        else:
            user = Friends.objects.all().filter(user_id=id).first()
            if request.method == 'GET':
                if user:
                    data = serializers.serialize('json', user.waiting_for_response.only('id','email','full_name','verfied','url_photo'))
                    cache.set("friend_request_list", data, timeout=CACHE_TTL)
                    _friends = user.waiting_for_response.values()
                    result = []
                    for i in _friends:
                        payload = {
                            'id': i['id'],
                            'email': i['email'],
                            'full_name': i['full_name'],
                            'verfied': i['verfied'],
                            'url_photo': i['url_photo']
                        }
                        result.append(payload)
                    response = {
                        'api_status': status.HTTP_200_OK,
                        'api_message': 'Friend request list berhasil',
                        'data': result
                    }
                    return JsonResponse(response, safe=False)
                else:
                    response = {
                        'api_status': status.HTTP_404_NOT_FOUND,
                        'api_messages': 'Friend request tidak ada'
                    }
                    return JsonResponse(response)
    except Exception as ex:
        response = {
            'error': status.HTTP_400_BAD_REQUEST,
            'status': ex.args
        }
        return JsonResponse(response)

@api_view(['PUT'])
def add_friend(request):
    """
    API Endpoint that allows user to request new-friend
    """
    try:
        user_id = int(request.query_params['user_id'])
        friend_id = int(request.query_params['friend_id'])
        if request.method == 'PUT':
            user = Friends.objects.all().filter(user_id=user_id).first()
            user_friend = Friends.objects.all().filter(user_id=friend_id).first()

            if user and user_friend:
                user.waiting_for_response.add(
                    Register.objects.get(id=friend_id))
                user_friend.friend_request.add(
                    Register.objects.get(id=user_id))

                msg = user.user_name + ' Send friend request to ' + user_friend.user_name + ', waiting for response now.'
                response = {
                    'api_status': status.HTTP_200_OK,
                    'api_messages': msg
                }
                return JsonResponse(response)
    except Exception as ex:
        response = {
            'error': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'status': ex.args
        }
        return JsonResponse(response)


@api_view(['PUT'])
def cancel_friend_request(request):
    try:
        user_id = int(request.query_params['user_id'])
        friend_id = int(request.query_params['friend_id'])

        if request.method == 'PUT':
            user = Friends.objects.all().filter(user_id=user_id).first()
            user_friend = Friends.objects.all().filter(user_id=friend_id).first()

            if user and user_friend:
                user.waiting_for_response.remove(friend_id)
                user_friend.friend_request.remove(user_id)

                msg = user.user_name + ' canceled friend request to ' + user_friend.user_name
                response = {
                    'api_status': status.HTTP_200_OK,
                    'api_messages': msg
                }
            return JsonResponse(response)

    except Exception as ex:
        response = {
            'error': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'status': ex.args
        }
        return JsonResponse(response)

# ignore friend request
@api_view(['PUT'])
def ignore_request(request):
    """
    API Endpoint that allows user to ignore-friend
    """
    try:
        user_id = int(request.query_params['user_id'])
        friend_id = int(request.query_params['friend_id'])
        if (request.method == 'PUT'):
            user = Friends.objects.all().filter(user_id=user_id).first()
            user_friend = Friends.objects.all().filter(user_id=friend_id).first()

            if user and user_friend:
                user.friend_request.remove(friend_id)
                user_friend.waiting_for_response.remove(user_id)

                msg = user.user_name + ' ignore ' + user_friend.user_name + ' friend request'
                response = {
                    'api_status': status.HTTP_200_OK,
                    'api_messages': msg
                }
                return JsonResponse(response)
    except Exception as ex:
        response = {
            'error': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'status': ex.args
        }
        return JsonResponse(response)


@api_view(['PUT'])
def accept_request(request):
    """
    API Endpoint that allows user to accept-friend
    """
    try:
        user_id = int(request.query_params['user_id'])
        friend_id = int(request.query_params['friend_id'])
        if (request.method == 'PUT'):
            user = Friends.objects.all().filter(user_id=user_id).first()
            if user:
                user.friend_request.remove(friend_id)
                user.friend_list.add(friend_id)
                user_friend = Friends.objects.all().filter(user_id=friend_id).first()
                user_friend.friend_list.add(user_id)
                user_friend.waiting_for_response.remove(user_id)

                msg = user.user_name + ' accept ' + user_friend.user_name + ' friend request'
                response = {
                    'api_status': status.HTTP_200_OK,
                    'api_messages': msg
                }
                return JsonResponse(response)
    except Exception as ex:
        response = {
            'error': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'status': ex.args
        }

        return JsonResponse(response)

# unfriend
@api_view(['PUT'])
def unfriend(request):
    """
    API Endpoint that allows user to unfriend
    """
    try:
        user_id = int(request.query_params['user_id'])
        friend_id = int(request.query_params['friend_id'])
        if (request.method == 'PUT'):
            user = Friends.objects.all().filter(user_id=user_id).first()
            if user:
                user.friend_list.remove(friend_id)
                user_friend = Friends.objects.all().filter(user_id=friend_id).first()
                user_friend.friend_list.remove(user_id)

                msg = user.user_name + ' unfriend ' + user_friend.user_name
                response = {
                    'api_status': status.HTTP_200_OK,
                    'api_messages': msg
                }
                return JsonResponse(response)
    except Exception as ex:
        response = {
            'error': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'status': ex.args
        }
        return JsonResponse(response)


@api_view(['GET'])
def suggestions(request):
    """
    API Endpoint that allows user to see friends-suggestion
    """

    try:
        if request.method == 'GET':
            _user = Register.objects.all()
            serializer = RegisterFriendsSerializers(_user, many=True)

            response = {
                'api_status': status.HTTP_200_OK,
                'api_messages': 'Friend suggestion for you',
                'data': serializer.data
            }

            return JsonResponse(response)
    except Exception as ex:
        response = {
            'error': status.HTTP_400_BAD_REQUEST,
            'status': str(ex.args)
        }
        return JsonResponse(response)

# search base on name
@api_view(['GET'])
def search(request, id, name):
    try:
        if (request.method == 'GET'):
            user = Friends.objects.all().filter(user_id=id).first()
            exclude_all = [int(id)]
            exclude_friend = list(user.friend_list.all().values_list(
                'id', flat=True).order_by('id'))
            exclude_friend_request = list(
                user.friend_request.all().values_list('id', flat=True).order_by('id'))
            exclude_waiting_for_response = list(
                user.waiting_for_response.all().values_list('id', flat=True).order_by('id'))
            for item in exclude_friend:
                exclude_all.append(int(item))
            for item in exclude_friend_request:
                exclude_all.append(int(item))
            for item in exclude_waiting_for_response:
                exclude_all.append(int(item))

            friend_suggestion = Register.objects.all().exclude(id__in=exclude_all)
            constrains = name.split("%")
            for constrain in constrains:
                search_result = friend_suggestion.filter(
                    full_name__icontains=constrain)
            serializer = RegisterSerializer(search_result, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as ex:
        response = {
            'error': str(ex),
            'status': ex.args
        }
        return JsonResponse(response)
