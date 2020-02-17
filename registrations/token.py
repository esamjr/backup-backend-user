import binascii
import os

from datetime import date

from django.conf import settings
from django.utils.http import int_to_base36
from django.utils.crypto import salted_hmac

key_salt = "django.contrib.auth.tokens.PasswordResetTokenGenerator"
secret = settings.SECRET_KEY


def make_token(register):
    set_token = _make_token_with_timestamp(register, _num_days(_today()))
    return_value = generate_key(set_token)
    return return_value


def _make_token_with_timestamp(register, timestamp):
        ts_b36 = int_to_base36(timestamp)
        hash = salted_hmac(
            key_salt,
            _make_hash_value(register, timestamp),
            secret=secret,
        ).hexdigest()[::2]  # Limit to 20 characters to shorten the URL.
        return "%s-%s" % (ts_b36, hash)


def _make_hash_value(register, timestamp):
    login_timestamp = '' if register.create_at is None else register.create_at.replace(microsecond=0, tzinfo=None)
    return str(register.id) + register.password + str(login_timestamp) + str(timestamp)


def _num_days(dt):
    return (dt - date(2001, 1, 1)).days


def _today():
    return date.today()


def generate_key(token):
    return binascii.hexlify(os.urandom(20)).decode()
