from django.http import JsonResponse
from rest_framework import status

from .models import Tokens

from datetime import timedelta, datetime
from django.utils import timezone
from django.conf import settings

_d = datetime.now()


# this return left time
def expires_in(token):
    _t = Tokens.objects.get(user_id__tokens__key=token)
    time_elapsed = timezone.now() - _t.created
    left_time = timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS) - time_elapsed
    return left_time


# token checker if token expired or not
def is_token_expired(request):
    cek_expire = expires_in(request)
    return cek_expire(request['key']) < timedelta(seconds=0)


# if token is expired new token will be established
# If token is expired then it will be removed
# and new one with different key will be created
def token_expire_handler(request):
    is_expired = is_token_expired(request)
    if is_expired:
        is_expired.delete()
        token = Tokens.objects.create(key=request['token'])
    return is_expired, token


def set_refresh_token(request):
    _r = Tokens.objects.filter(user_id=request.pk).exists()
    if not _r:
        return False
    else:
        Tokens.objects.get(user_id=request.pk).delete()
        return False


def cek_expire_tokens(token):
    _t = Tokens.objects.get(key=token)
    time_elapsed = timezone.now() - _t.created
    left_time = timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS) - time_elapsed

    _cek_expire = left_time < timedelta(seconds=0)

    return _cek_expire


def is_authentication(token):

    _data = token

    if _data == '' or _data is None:
        response = {
            'api_status': status.HTTP_401_UNAUTHORIZED,
            'api_message': 'Token user tidak ada'
        }

        return JsonResponse(response)

    _cek_token = Tokens.objects.filter(key=_data).exists()
    if not _cek_token:
        response = {
            'api_status': status.HTTP_404_NOT_FOUND,
            'api_message': 'Token tidak sama atau sudah logout sebelumnya'
        }

        return JsonResponse(response)

    _is_token = Tokens.objects.get(key=_data)

    return _is_token
