from rest_framework import status

from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.hashers import check_password


from vendor_api.models import MultipleLogin, Vendor_api
from .models import Register, Tokens

from vendor_api.serializers import MultipleSerializer
from .serializers import LoginSerializer


def get_json_list(query_set):
    list_objects = []
    for obj in query_set:
        dict_obj = {}
        for field in obj._meta.get_fields():
            try:
                if field.many_to_many:
                    dict_obj[field.name] = get_json_list(getattr(obj, field.name).all())
                    continue
                dict_obj[field.name] = getattr(obj, field.name)
            except AttributeError:
                continue
        list_objects.append(dict_obj)
    return list_objects


def delete_all_tokens(id_user):
    _m = MultipleLogin.objects.get(id_user=id_user)

    payload = {
        'id_user': _m.id_user,
        'token_web': 'xxx',
        'token_phone': 'xxx'
    }

    serializer = MultipleSerializer(_m, data=payload)
    if serializer.is_valid():
        serializer.save()

    _cek_t = Tokens.objects.filter(user_id=id_user).exists()
    if _cek_t:
        _t = Tokens.objects.get(user_id=id_user)
        if _t:
            _t.delete()

    # code will be remove after token already fix for migrations
    _r = Register.objects.get(id=id_user)
    get_out = {
        'email': _r.email,
        'password': _r.password,
        'id_type': 0,
        'token': 'xxx',
        'attempt': 0
    }
    serializer = LoginSerializer(_r, data=get_out)
    if serializer.is_valid():
        serializer.save()
    # end of old code


def cek_password(password, _user):
    _salt = ''.join(str(ord(c)) for c in _user.full_name)
    _pass = password + _salt
    response = check_password(_pass, _user.password)

    return response


def logout_vendor(request):
    beacon_multi = MultipleLogin.objects.get(id_user=request.user_id_id)
    if not beacon_multi:
        response = {
            'api_status': status.HTTP_400_BAD_REQUEST,
            'api_message': 'Id User ada tidak terdaftar di Multiple Login'
        }

        return JsonResponse(response)

    payload = {
        'id_user': beacon_multi.id_user,
        'token_web': beacon_multi.token_web,
        'token_phone': 'xxx'
    }

    serializer = MultipleSerializer(beacon_multi, data=payload)

    if serializer.is_valid():
        serializer.save()

    return serializer
