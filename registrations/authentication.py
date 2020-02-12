import datetime
from django.utils.timezone import utc

from .models import Tokens

from datetime import timedelta
from django.utils import timezone
from django.conf import settings


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
