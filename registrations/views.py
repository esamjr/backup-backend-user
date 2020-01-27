import time
import requests
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password, make_password
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

from email_app.views import send_email, send_forget_email, send_registration_email
from log_app.views import update_log, read_log
from vendor_api.models import MultipleLogin
from vendor_api.serializers import MultipleSerializer
from .models import Register
from .serializers import RegisterSerializer, LoginSerializer, MaxAttemptReachSerializer, \
    ConfirmSerializer, PassingAttemptSerializer, ForgetSerializer, AttemptSerializer, SentForgetSerializer, \
    SearchSerializer, UserSerializer


@api_view(['POST'])
def upload_xls(request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION')
        admin = Register.objects.get(token=token)
        if admin.id == 0:
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                payload_domo = {
                    'id_user': serializer.data['id'],
                    'status_domoo': 0
                }
                serialdomo = DomoSerializer(data=payload_domo)
                if serialdomo.is_valid():
                    serialdomo.save()
                    payload_multilogin = {
                        'id_user': serializer.data['id'],
                        'token_web': serializer.data['token'],
                        'token_phone': 'xxx'
                    }
                    serializer_multi = MultipleSerializer(data=payload_multilogin)
                    if serializer_multi.is_valid():
                        serializer_multi.save()
                        subjects = 'Activation account'
                        try:
                            send_email(request, serializer.data['email'], serializer.data['token'],
                                       serializer.data['full_name'], subjects)
                        except:
                            return Response({'error in here'})
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer_multi.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response(serialdomo.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': 'User Is Unauthorized, because its not admin id'},
                            status=status.HTTP_401_UNAUTHORIZED)
    except Register.DoesNotExist:
        return Response({'status': 'User Is Does not exist'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def get_search_by_name(request):
    if request.method == 'POST':
        name = request.data['name']
        if not name:
            network = Register.objects.all()
            serializer = RegisterSerializer(network, many=True)
            return Response(serializer.data)
        else:
            network = Register.objects.all().filter(full_name__icontains=name)
            serializer = RegisterSerializer(network, many=True)
            return Response(serializer.data)


@api_view(['GET'])
def get_user_by_email(request, pk):
    """
    function get data by email
    :param pk:
    :param request: email
    :return: if email already exist in employee, return data null
    """
    token = request.META.get('HTTP_AUTHORIZATION', '')
    get_token = Register.objects.get(token=token)
    if request.method == "GET":
        registrations = Register.objects.get(pk=pk)
        serializer = SearchSerializer(registrations)
        act = 'searching user id ' + str(pk)
        read_log(request, get_token, act)

        if not serializer.errors:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_user(request, pk):
    token = request.META.get('HTTP_AUTHORIZATION', '')
    get_token = Register.objects.get(token=token)
    if request.method == 'GET':
        registrations = Register.objects.get(pk=pk)
        serializer = SearchSerializer(registrations)
        act = 'searching user id ' + str(pk)
        read_log(request, get_token, act)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
def get_delete_update_registrations(request, pk):
    try:
        registrations = Register.objects.get(pk=pk)
        if (registrations.token == 'xxx'):
            response = {'status': 'LOGIN FIRST, YOU MUST...'}
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:

                if request.method == 'GET':
                    serializer = RegisterSerializer(registrations)
                    return Response(serializer.data)

                elif request.method == 'DELETE':
                    Register.delete()
                    content = {
                        'status': 'NO CONTENT'
                    }
                    return Response(content, status=status.HTTP_204_NO_CONTENT)

                elif request.method == 'PUT':
                    serializer = RegisterSerializer(registrations, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        payload = {
                            'id': serializer.data['id'],
                            'name': serializer.data['full_name'],
                            'photo': serializer.data['url_photo']
                        }
                        url = 'http://x-attandance.mindzzle.com/api/user_update'
                        Req = requests.post(url, data=payload)
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            except Register.DoesNotExist:
                response = {'status': 'Invalid Token'}
                return Response(response, status=status.HTTP_404_NOT_FOUND)

    except Register.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def search(request):
    if request.method == 'POST':
        name = request.data['name']
        if (name == None):
            network = Register.objects.all()
            serializer = RegisterSerializer(network, many=True)
            return Response(serializer.data)
        else:
            network = Register.objects.all().filter(full_name__icontains=name)
            serializer = RegisterSerializer(network, many=True)
            return Response(serializer.data)


@api_view(['GET', 'POST'])
def get_post_registrations(request):
    if request.method == 'GET':
        name = request.data['name']
        if (name == None):
            network = Register.objects.all()
            serializer = RegisterSerializer(network, many=True)
            return Response(serializer.data)
        else:
            network = Register.objects.all().filter(full_name__icontains=name)
            serializer = RegisterSerializer(network, many=True)
            return Response(serializer.data)
    elif request.method == 'POST':
        email = request.data['email']
        email_var = email.lower()
        password = request.data['password']
        name = request.data['full_name']
        salt_password = ''.join(str(ord(c)) for c in name)
        id_type = 0
        banned_type = "0"
        token = make_password(str(time.time()))
        hs_pass = make_password(str(password) + str(salt_password))
        payload = {
            'full_name': name,
            'email': email_var,
            'salt_password': salt_password,
            'password': hs_pass,
            'primary_phone': request.data['primary_phone'],
            'primary_address': request.data['primary_address'],
            'id_country': request.data['id_country'],
            'id_regions': request.data['id_regions'],
            'tax_num': request.data['tax_num'],
            'url_photo': request.data['url_photo'],
            'description': request.data['description'],
            'id_type': id_type,
            'banned_type': banned_type,
            'birth_day': request.data['birth_day'],
            'id_city': request.data['id_city'],
            'token': token
        }

        serializer = RegisterSerializer(data=payload)
        if serializer.is_valid():
            serializer.save()
            # payload_domo = {
            #     'id_user': serializer.data['id'],
            #     'status_domoo': 0
            # }
            # serialdomo = DomoSerializer(data=payload_domo)
            # if serialdomo.is_valid():
            #     serialdomo.save()
            #     payload_multilogin = {
            #         'id_user': serializer.data['id'],
            #         'token_web': serializer.data['token'],
            #         'token_phone': 'xxx'
            #     }
            #     serializer_multi = MultipleSerializer(data=payload_multilogin)
            #     if serializer_multi.is_valid():
            #         serializer_multi.save()

            try:
                request = {
                    'mail': email,
                    'subjects': "Activation Email!",
                    'name': name,
                    'token': token
                }

                send_registration_email(request)
            except:
                return Response({'error in here'})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def forget_attempt(request, email):
    if request.method == 'POST':
        token_forget = 'usethistokenforforgetyourpassword'
        tokenx = str(token_forget)
        token = make_password(tokenx)

        try:
            check = Register.objects.get(email=email)
            name = check.full_name

            if (check.attempt >= 25):
                token_max_attempt = make_password(
                    'this is the maximum reach token, unfortunately we must banned this account temporarly')
                payload = {'token': token_max_attempt, 'password': token_max_attempt, 'attempt': 0}
                serializers = MaxAttemptReachSerializer(check, data=payload)
                if serializers.is_valid():
                    serializers.save()
                    # response = {'status':'you have reach your maximum attempt in one day, please try again in 24 hours'}
                response = {'status': '2'}
                return Response(response)
            else:
                counter = check.attempt + 1
                payload = {'token': token, 'attempt': counter}
                serializers = PassingAttemptSerializer(check, data=payload)
                if serializers.is_valid():
                    serializers.save()
                else:
                    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
            subjects = 'Forget Password by try to reach the password'
            send_forget_email(request, email, token, name, subjects)
            act = 'User reach maximum attempt by '
            read_log(request, check, act)
            response = {'status': '1'}
            return Response(response)
            # return Response({'status':'Your password is incorrect, please check your email to make new password'})
        except Register.DoesNotExist:
            response = {'status': 'Email Does not valid'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
def attempt_login(request, email):
    attempt = Register.objects.get(email=email)
    counter = attempt.attempt + 1
    payload = {'attempt': counter}
    serializer = AttemptSerializer(attempt, data=payload)
    if serializer.is_valid():
        serializer.save()
        return Response(counter)
    return Response(serializer.errors)


@api_view(['POST', 'GET'])
def get_login(request):
    try:
        if request.method == 'POST':
            emails = request.data['email']
            email = emails.lower()
            key = request.data['password']
            beacon = Register.objects.get(email=email)
            salt = beacon.full_name
            salt_password = ''.join(str(ord(c)) for c in salt)
            password = key + salt_password
            token = make_password(str(time.time()))
            token_forget = 'usethistokenforforgetyourpassword'
            tokenx = str(token_forget)
            get_login = Register.objects.get(email=email)
            attempt = get_login.attempt
            if (check_password(tokenx, get_login.token)):
                response = {'status': 'you request to change your password, please check your email'}
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)
            elif (get_login.banned_type == "0"):
                response = {'status': 'Account has not verified yet, check your email to verified'}
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)
            elif (check_password(password, get_login.password)):
                flag = beacon.banned_type
                get_in = {
                    'email': get_login.email,
                    'password': get_login.password,
                    'id_type': 1,
                    'banned_type': "1",
                    'token': token,
                    'attempt': 1
                }
                serializer = LoginSerializer(get_login, data=get_in)
                if serializer.is_valid():
                    act = 'user logging in by '
                    read_log(request, get_login, act)
                    serializer.save()
                    response = {
                        'status': 'SUCCESSFULLY LOGIN',
                        'token': get_login.token,
                        'id_user': get_login.id,
                        'email': get_login.email,
                        'flag ': flag
                    }
                    try:
                        beacon_multi = MultipleLogin.objects.get(id_user=get_login.id)
                        payload_multilogin = {
                            'id_user': get_login.id,
                            'token_web': serializer.data['token'],
                            'token_phone': 'xxx'
                        }
                        serializer_multi = MultipleSerializer(beacon_multi, data=payload_multilogin)
                        if serializer_multi.is_valid():
                            serializer_multi.save()
                    except MultipleLogin.DoesNotExist:
                        payload_multilogin = {
                            'id_user': get_login.id,
                            'token_web': serializer.data['token'],
                            'token_phone': 'xxx'
                        }
                        serializer_multi = MultipleSerializer(data=payload_multilogin)
                        if serializer_multi.is_valid():
                            serializer_multi.save()
                    return Response(response, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                if (attempt == 0):
                    attempt_login(request, email)
                    response = {'status': 'Wrong Username / Password'}
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
                elif (attempt % 5 == 0):
                    forget_attempt(request, email)
                    return Response(forget_attempt, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    attempt_login(request, email)
                    response = {'status': 'Wrong Username / Password'}
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'GET':
            token = request.META.get('HTTP_AUTHORIZATION')
            get_token = Register.objects.get(token=token)
            Registration = get_token.id
            if (get_token.id == Registration):
                get_out = {
                    'email': get_token.email,
                    'password': get_token.password,
                    'id_type': 0,
                    'token': 'xxx',
                    'attempt': 0
                }
                serializer = LoginSerializer(get_token, data=get_out)
                if serializer.is_valid():
                    act = 'user has logout by '
                    read_log(request, get_token, act)
                    serializer.save()
                    response = {'status': 'SUCCESSFULLY LOGOUT'}
                    try:
                        beacon_multi = MultipleLogin.objects.get(id_user=get_token.id)
                        payload_multilogin = {
                            'id_user': Registration,
                            'token_web': 'xxx',
                            'token_phone': get_token.token
                        }
                        serializer_multi = MultipleSerializer(beacon_multi, data=payload_multilogin)
                        if serializer_multi.is_valid():
                            serializer_multi.save()
                    except MultipleLogin.DoesNotExist:
                        pass
                    return Response(response, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            response = {'status': 'NOT FOUND 1'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        else:
            response = {'status': 'BAD REQUEST'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
    except Register.DoesNotExist:
        response = {'status': 'NOT FOUND'}
        return Response(response, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def verified_acc(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            get_token = Register.objects.get(token=token)
            payload = {
                'banned_type': "2"
            }
            serializer = ConfirmSerializer(get_token, data=payload)
            if serializer.is_valid():
                act = 'user has verified account with name : '
                read_log(request, get_token, act)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Register.DoesNotExist:
            response = {'status': 'NOT FOUND'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def forget(request):
    if request.method == 'POST':
        token_forget = 'usethistokenforforgetyourpassword'
        tokenx = str(token_forget)
        token = make_password(tokenx)
        email = request.data['email']
        payload = {'token':token}
        try:
            check = Register.objects.get(email= email)
            serializers = SentForgetSerializer(check, data = payload)
            if serializers.is_valid():
                serializers.save()
            else:
                return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

            request = {
                'mail': email,
                'subjects': 'Forget Password',
                'name': check.full_name,
                'token': token
            }

            send_forget_email(request)

            return Response({'status': 'Email already sent'})
        except Register.DoesNotExist:
            response = {'status':'Email Does not valid'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def forget_backlink(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            get_token = Register.objects.get(token=token)
            token = make_password(str(time.time()))
            salt = get_token.full_name
            salt_password = ''.join(str(ord(c)) for c in salt)
            password = request.data['password']
            hs_pass = make_password(str(password) + str(salt_password))
            payload = {'password': hs_pass, 'token': token}
            serializers = ForgetSerializer(get_token, data=payload)
            if serializers.is_valid():
                serializers.save()
                act = 'password is changed by '
                update_log(request, get_token, act)
                response = {'status': 'Password chaged'}
                return Response(response, status=status.HTTP_201_CREATED)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        except Register.DoesNotExist:
            response = {'status': 'Your token is invalid'}
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)


@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if email is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)

    user = authenticate(username=email, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)

