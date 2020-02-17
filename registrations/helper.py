from rest_framework import status
from django.http import JsonResponse
from django.conf import settings

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


def delete_all_tokens(_token, user_id, token_ven):
    _m = MultipleLogin.objects.get(id_user=user_id)
    _get_m = Vendor_api.objects.get(token=token_ven)
    if _get_m.username == settings.MINDZZLE_USERNAME:
        payload = {
            'id_user': _m.id_user,
            'token_web': 'xxx',
            'token_phone': _m.token_phone
        }

        serializer = MultipleSerializer(_m, data=payload)
        if serializer.is_valid():
            serializer.save()
    elif _get_m.username == settings.CROCODIC_USERNAME:
        payload = {
            'id_user': _m.id_user,
            'token_web': _m.token_web,
            'token_phone': 'xxx'
        }

        serializer = MultipleSerializer(_m, data=payload)
        if serializer.is_valid():
            serializer.save()
    else:
        response = {
            "api_status": status.HTTP_404_NOT_FOUND,
            "api_message": 'Token vendor tidak ditemukan',
        }

        return JsonResponse(response)

    _t = Tokens.objects.get(key=_token, user_id=user_id)
    if _t:
        _t.delete()

    # code will be remove after token already fix for migrations
    _r = Register.objects.get(id=user_id)
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
