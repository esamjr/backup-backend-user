from django.http import JsonResponse
from rest_framework import status

from .models import Business


def cek_company_id(request):
    _cek_company = Business.objects.filter(id=request).exists()
    if not _cek_company:
        return False
    return True


def _company_id(request):
    _cek_comp = Business.objects.filter(id=request).exists()
    if not _cek_comp:
        response = {
            'api_status': status.HTTP_400_BAD_REQUEST,
            'api_message': 'id company tidak terdaftar'
        }

        return JsonResponse(response)

    _company = Business.objects.get(id=request)

    return _company
