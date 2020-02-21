import time
import requests

from datetime import datetime

from django.contrib.auth.hashers import check_password, make_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from email_app.views import send_email, send_forget_email, send_registration_email
from log_app.views import read_log
from join_company.models import Joincompany
from vendor_api.models import MultipleLogin, Vendor_api
from vendor_api.serializers import MultipleSerializer

from .helper import get_json_list, delete_all_tokens, cek_password
from .token import make_token
from .authentication import expires_in, set_refresh_token, cek_expire_tokens

from .models import Register, Tokens
from .serializers import RegisterSerializer, LoginSerializer, MaxAttemptReachSerializer, \
    ConfirmSerializer, PassingAttemptSerializer, ForgetSerializer, AttemptSerializer, SentForgetSerializer, \
    SearchSerializer, TokensSerializer, TokenSerializer


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
    # token = request.META.get('HTTP_AUTHORIZATION')
    # get_token = Register.objects.get(token=token)
    if request.method == "GET":
        _token = request.META.get('HTTP_AUTHORIZATION')
        if _token == "":
            response = {
                'api_status': status.HTTP_400_BAD_REQUEST,
                'api_message': "Token tidak ada",

            }

            return JsonResponse(response)

        _cek_token = Tokens.objects.filter(key=_token).exists()
        if not _cek_token:
            response = {
                'api_status': status.HTTP_400_BAD_REQUEST,
                'api_message': "Token expire",
            }

            return JsonResponse(response)

        _cek_user = Register.objects.filter(pk=pk).exists()
        if not _cek_user:
            response = {
                'api_status': status.HTTP_404_NOT_FOUND,
                'api_message': "User tidak terdaftar",
            }

            return JsonResponse(response)

        registrations = Register.objects.get(pk=pk)
        serializer = SearchSerializer(registrations)

        response = {
            'api_status': status.HTTP_201_CREATED,
            'api_message': "Email aktivasi terkirim",
            'data': {
                serializer.data
            }
        }

        return JsonResponse(response)

    resp_error = {
        'api_status': status.HTTP_400_BAD_REQUEST,
        'api_message': "Email aktivasi error",
    }

    return JsonResponse(resp_error)


@api_view(['GET'])
def get_user(request, pk):
    token = request.META.get('HTTP_AUTHORIZATION', '')
    # get_token = Register.objects.get(token=token)
    if request.method == 'GET':
        registrations = Register.objects.get(pk=pk)
        serializer = SearchSerializer(registrations)
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
        if name == None:
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
        id_user = request.query_params['id_user']
        if id_user == "" or id_user is None:
            network = Register.objects.all()
            serializer = RegisterSerializer(network, many=True)
            return Response(serializer.data)
        else:
            # network = Register.objects.all().filter(full_name__icontains=name)
            network = Register.objects.all().filter(id=id_user)
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
            'token': 'xxx'
        }

        serializer = RegisterSerializer(data=payload)
        if serializer.is_valid():
            serializer.save()

            _get_user_data = Register.objects.get(email=email)
            _token = make_token(_get_user_data)

            set_in = {
                    'user_id': _get_user_data.id,
                    'key': _token,
                }

            serializer = TokensSerializer(data=set_in)

            if serializer.is_valid():
                serializer.save()

            # code will be remove after token already fix for migrations
            handle_registrasi_old_token(_get_user_data, _token)
            # end of old code

            request = {
                'mail': email,
                'subjects': "Activation Email!",
                'name': name,
                'token': _token
            }

            send_registration_email(request)

            response = {
                'api_status': status.HTTP_201_CREATED,
                'api_message': "Email aktivasi terkirim",

            }

            return JsonResponse(response)

        resp_error = {
            'api_status': status.HTTP_400_BAD_REQUEST,
            'api_message': "Email aktivasi tidak bisa terkirim",
        }

        return JsonResponse(resp_error)


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
def activate_email(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION')
        if token == "":
            response = {
                'api_status': status.HTTP_401_UNAUTHORIZED,
                'api_message': 'Token tidak ada'
            }

            return JsonResponse(response)

        _token = Tokens.objects.filter(key=token).exists()
        if not _token:
            response = {
                'api_status': status.HTTP_408_REQUEST_TIMEOUT,
                'api_message': 'Token sudah berubah'
            }

            return JsonResponse(response)

        _set_token = Tokens.objects.get(key=token)
        get_token = Register.objects.get(id=_set_token.user_id_id)

        payload = {
            'banned_type': "2"
        }

        serializer = ConfirmSerializer(get_token, data=payload)

        if serializer.is_valid():
            serializer.save()

            response = {
                'api_status': status.HTTP_201_CREATED,
                'api_message': 'Verifikasi berhasil.'
            }

            return JsonResponse(response)

        response = {
            'api_status': status.HTTP_404_NOT_FOUND,
            'api_message': 'Verifikasi gagal dilakukan.'
        }

        return Response(response)


@api_view(['POST'])
def forget(request):
    if request.method == 'POST':
        email = request.data['email']
        _check_email = Register.objects.filter(email=email).exists()
        if not _check_email:
            response = {
                'api_status': status.HTTP_404_NOT_FOUND,
                'api_message': "Email belum terdaftar"
            }

            return JsonResponse(response)

        check = Register.objects.get(email=email)

        _token = make_token(check)

        # code will be remove after token already fix for migrations
        payload = {
            'token': _token
        }

        serializers = SentForgetSerializer(check, data=payload)
        if serializers.is_valid():
            serializers.save()
        # end of old code

        set_in = {
            'user_id': check.id,
            'key': _token,
        }

        _cek_token = set_refresh_token(check)

        _token_serializer = TokensSerializer(data=set_in)

        if _token_serializer.is_valid():
            _token_serializer.save()

        request = {
            'mail': email,
            'subjects': 'Forget Password',
            'name': check.full_name,
            'token': _token
        }

        send_forget_email(request)

        response = {
            'api_status': status.HTTP_201_CREATED,
            'api_message': "Email sudah terkirim"
        }

        return JsonResponse(response)


@api_view(['POST'])
def forget_backlink(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION')

        _get_token = Register.objects.filter(token=token).exists()
        if not _get_token:
            response = {
                'api_status': status.HTTP_404_NOT_FOUND,
                'api_message': "Token sudah habis masa aktivnya"
            }

            return JsonResponse(response)

        check = Register.objects.get(token=token)

        _token = make_token(check)

        # code will be remove after token already fix for migrations
        password = request.data['password']

        _set_token = make_password(str(time.time()))
        salt = check.full_name
        salt_password = ''.join(str(ord(c)) for c in salt)
        hs_pass = make_password(str(password) + str(salt_password))

        payload = {
            'password': hs_pass,
            'token': _token
        }

        serializers = ForgetSerializer(check, data=payload)
        if serializers.is_valid():
            serializers.save()
        # end of old code

        set_in = {
            'user_id': check.id,
            'key': _token,
        }

        _cek_token = set_refresh_token(check)

        _token_serializer = TokensSerializer(data=set_in)

        if _token_serializer.is_valid():
            _token_serializer.save()

        response = {
            'api_status': status.HTTP_201_CREATED,
            'api_message': "Password sudah berubah"
        }

        return JsonResponse(response)


@api_view(['GET'])
def login_token_views(request):
    token_meta = request.META.get('HTTP_AUTHORIZATION')
    _token = Vendor_api.objects.filter(token=token_meta).exists()
    if not _token:
        response = {
            'api_status': status.HTTP_400_BAD_REQUEST,
            'api_message': 'Token Vendor salah'
        }

        return JsonResponse(response)

    email = request.data.get("email")
    password = request.data.get("password")

    if email == ""or password == "":
        response = {
            'api_status': status.HTTP_400_BAD_REQUEST,
            'api_message': 'Password atau Email tidak bisa kosong'
        }

        return JsonResponse(response)

    _check_email = Register.objects.filter(email=email).exists()
    if not _check_email:
        response = {
            'api_status': status.HTTP_404_NOT_FOUND,
            'api_message': "Email belum terdaftar"
        }

        return JsonResponse(response)

    _get_user_data = Register.objects.get(email=email)
    _salt = ''.join(str(ord(c)) for c in _get_user_data.full_name)
    _pass = password + _salt
    _check_password = check_password(_pass, _get_user_data.password)

    if not _check_password:
        response = {
            'api_status': status.HTTP_404_NOT_FOUND,
            'api_message': "Password salah"
        }

        return JsonResponse(response)

    _get_phone = MultipleLogin.objects.get(id_user=_get_user_data.id)
    _get_id_company = Joincompany.objects.filter(id_user=_get_user_data.id)

    response = {
        'api_status': status.HTTP_200_OK,
        'api_message': "Successfully sent",
        "email": _get_user_data.email,
        "token_web": _get_user_data.token,
        "token_phone": _get_phone.token_phone,
        "id_company": get_json_list(_get_id_company)
    }

    return JsonResponse(response, content_type='application/json')


@api_view(['POST', 'GET'])
def cek_login_views(request):
    response = None
    if request.method == 'POST':
        email = request.data['email']
        password = request.data['password']

        if email == "" or password == "":
            response = {
                'api_status': status.HTTP_400_BAD_REQUEST,
                'api_message': 'email atau password tidak bisa kosong!'
            }
            return JsonResponse(response)

        _cek_email = Register.objects.filter(email=email).exists()
        if not _cek_email:
            response = {
                'api_status': status.HTTP_404_NOT_FOUND,
                'api_message': 'email belum terdaftar'
            }

            return JsonResponse(response)

        _get_user_data = Register.objects.get(email=email)

        if _get_user_data.banned_type == "0":
            response = {
                'api_status': status.HTTP_401_UNAUTHORIZED,
                'api_message': 'Account Belum diverifikasi, silahkan cek email untuk verifikasi'
            }

            return JsonResponse(response)

        _check_banned = Register.objects.filter(email=email).values('banned_type')

        _cek_password = cek_password(password, _get_user_data)
        if not _cek_password:
            response = {
                'api_status': status.HTTP_400_BAD_REQUEST,
                'api_message': 'Password tidak sesuai'
            }

            return JsonResponse(response)

        flag = _get_user_data.banned_type

        _cek_token = set_refresh_token(_get_user_data)

        _token = make_token(_get_user_data)

        set_in = {
            'user_id': _get_user_data.id,
            'key': _token,
        }

        serializer = TokensSerializer(data=set_in)

        if serializer.is_valid():
            serializer.save()

            _update_vendor_login = update_vendor_login(_get_user_data, _token)

            # code will be remove after token already fix for migrations
            handle_login_old_token(_get_user_data, _token)
            # end of old code

            response = {
                "api_status": status.HTTP_202_ACCEPTED,
                "api_message": 'Login Berhasil',
                "user": {
                    'id_user': _get_user_data.id,
                    'email': _get_user_data.email,
                    'flag ': flag,

                },
                "expires_in": str(expires_in(_token)),
                "token": _token
            }

        return JsonResponse(response)

    elif request.method == 'GET':
        token = request.META.get('HTTP_AUTHORIZATION')
        _cek_token = Tokens.objects.filter(key=token).exists()
        if not _cek_token:
            response = {
                'api_status': status.HTTP_404_NOT_FOUND,
                'api_message': 'Anda telah logout sebelumnya'
            }

            return JsonResponse(response)

        _cek_data = Tokens.objects.get(key=token)

        # code will be remove after token already fix for migrations
        handle_logout_old_token(_cek_data.key)

        _logout_vendor_login = logout_vendor_login(_cek_data)
        _cek_data.delete()

        response = {
            'api_status': status.HTTP_200_OK,
            'api_message': 'Successfully logged out.'
        }

        return JsonResponse(response)


def handle_registrasi_old_token(_get_user_data, token):
    get_in = {
        'token': token,
    }

    serializer = TokenSerializer(_get_user_data, data=get_in)
    if serializer.is_valid():
        serializer.save()


def handle_login_old_token(_get_user_data, token):
    get_in = {
        'email': _get_user_data.email,
        'password': _get_user_data.password,
        'id_type': 1,
        'banned_type': "1",
        'token': token,
        'attempt': 1
    }

    serializer = LoginSerializer(_get_user_data, data=get_in)
    if serializer.is_valid():
        serializer.save()


def handle_logout_old_token(token):
    _cek_data = Register.objects.get(token=token)
    get_out = {
        'email': _cek_data.email,
        'password': _cek_data.password,
        'id_type': 0,
        'token': 'xxx',
        'attempt': 0
    }
    serializer = LoginSerializer(_cek_data, data=get_out)
    if serializer.is_valid():
        serializer.save()


def update_vendor_login(request, _token):
    _cek_multi = MultipleLogin.objects.filter(id_user=request.id).exists()
    if not _cek_multi:
        payload_multilogin = {
            'id_user': request.id,
            'token_web': _token,
            'token_phone': 'xxx'
        }
        _new_multi = MultipleSerializer(data=payload_multilogin)
        if _new_multi.is_valid():
            _new_multi.save()

            return _new_multi

    payload_multi_login = {
        'id_user': request.id,
        'token_web': _token,
        'token_phone': 'xxx'
    }

    beacon_multi = MultipleLogin.objects.get(id_user=request.id)
    serializer_multi = MultipleSerializer(beacon_multi, data=payload_multi_login)
    if serializer_multi.is_valid():
        serializer_multi.save()

    return serializer_multi


def logout_vendor_login(request):
    beacon_multi = MultipleLogin.objects.get(id_user=request.user_id_id)
    if not beacon_multi:
        response = {
            'api_status': status.HTTP_400_BAD_REQUEST,
            'api_message': 'Id User ada tidak terdaftar di Multiple Login'
        }

        return JsonResponse(response)

    payload = {
        'id_user': beacon_multi.id_user,
        'token_web': 'xxx',
        'token_phone': 'xxx'
    }

    serializer = MultipleSerializer(beacon_multi, data=payload)

    if serializer.is_valid():
        serializer.save()

    return serializer


@api_view(['GET'])
def cek_token_expire(request):
    params = None

    if request.method == "GET":
        """
        function for check if token alredy expire
        :param id:
        :return: true or false
        """

        params = {
            'id_user': int(request.query_params['id_user']),
            'token': request.query_params['token'],
        }

        _u = Tokens.objects.filter(user_id=params['id_user']).exists()
        if not _u:
            response = {
                'api_status': status.HTTP_404_NOT_FOUND,
                'api_message': 'User sudah logout.'
            }

            return JsonResponse(response)

        _t = Tokens.objects.get(key=params['token'], user_id=params['id_user'])
        if _t == "":
            response = {
                'api_status': status.HTTP_404_NOT_FOUND,
                'api_message': 'Token sudah berubah.'
            }

            return JsonResponse(response)

        _c = cek_expire_tokens(params['token'])
        if _c:
            delete_all_tokens(params['token'])

            response = {
                "api_status": status.HTTP_201_CREATED,
                "api_message": 'Token habis masa aktivnya',
            }

            return JsonResponse(response)

    response = {
        "api_status": status.HTTP_200_OK,
        "api_message": 'Token masih aktive',
        "id_user": params['id_user'],
        "token": params['token'],
        "expires_in": str(expires_in(params['token'])),
    }

    return JsonResponse(response)
