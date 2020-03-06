import datetime

from django.db import transaction
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from business_account.helper import cek_company_id

from .models import BillingLicense
from .serializers import BillingLicenseSerializer, BillingLicenseAllDataSerializer


@api_view(['GET', 'POST', 'PUT'])
def billing_license_list(request):
    """
    API endpoint that allows Billing to be List all or create a new license..
    """
    try:
        id_company = request.data['id_company']
        _is_company = cek_company_id(id_company)

        if not _is_company:
            response = {
                'api_status': status.HTTP_404_NOT_FOUND,
                'api_message': 'Company tidak ada',
            }

            return JsonResponse(response)

        if request.method == 'GET':
            _billing = BillingLicense.objects.all()
            serializer = BillingLicenseAllDataSerializer(_billing, many=True)

            response = {
                'api_status': status.HTTP_200_OK,
                'api_message': 'Ambil data biling sukses',
                'data': serializer.data
            }

            return JsonResponse(response)

        elif request.method == 'POST':
            serializer = BillingLicenseSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

            response = {
                'api_status': status.HTTP_200_OK,
                'api_message': 'input data berhasil',
                'data': serializer.data
            }

            return JsonResponse(response)

        elif request.method == 'PUT':
            id_billing = request.data['id_billing']
            new_qty = request.data['qty_license']

            _cek_license = BillingLicense.objects.filter(id=id_billing).exists()
            if not _cek_license:
                response = {
                    'api_status': status.HTTP_404_NOT_FOUND,
                    'api_message': 'License Company tidak ada',
                }

                return JsonResponse(response)

            _cek_license_ex = BillingLicense.objects.get(id=id_billing)
            if not _cek_license_ex.status_license:
                response = {
                    'api_status': status.HTTP_401_UNAUTHORIZED,
                    'api_message': 'Status license Company tidak aktif',
                }

                return JsonResponse(response)

            """ function for get and update qty """
            _get_data = BillingLicense.objects.get(id=id_billing)
            old_qty = _get_data.qty_license

            _t = datetime.datetime.now()

            with transaction.atomic():
                BillingLicense.objects.filter(id=id_billing).update(qty_license=new_qty + old_qty,
                                                                    update_date=_t)

            response = {
                'api_status': status.HTTP_200_OK,
                'api_message': 'Update data berhasil',
            }

            return JsonResponse(response)
    except Exception as ex:
        response = {
            'error': str(ex),
            'status': ex.args
        }

        return JsonResponse(response)


@api_view(['PUT'])
def update_license_date(request):
    """
    API endpoint for handle expire datetime order by company_id
    """
    try:
        id_company = request.data['id_company']
        _is_company = cek_company_id(id_company)

        if not _is_company:
            response = {
                'api_status': status.HTTP_404_NOT_FOUND,
                'api_message': 'Company tidak ada',
            }

            return JsonResponse(response)

    except Exception as ex:
        response = {
            'error': str(ex),
            'status': ex.args
        }

        return JsonResponse(response)


@api_view(['PUT'])
def update_qty_license(request):
    """
    API endpoint for update qty base on in_company
    """
    try:
        id_company = request.data['id_company']
        _is_company = cek_company_id(id_company)

        if not _is_company:
            response = {
                'api_status': status.HTTP_404_NOT_FOUND,
                'api_message': 'Company tidak ada',
            }

            return JsonResponse(response)

        id_billing = request.data['id_billing']

        _get_data = BillingLicense.objects.get(id=id_billing)
        old_qty = _get_data.qty_license

        if old_qty == 0:
            response = {
                'api_status': status.HTTP_400_BAD_REQUEST,
                'api_message': 'License sudah habis',
            }

            return JsonResponse(response)

        with transaction.atomic():
            BillingLicense.objects.filter(id=id_billing).update(qty_license=old_qty - 1)

        response = {
            'api_status': status.HTTP_200_OK,
            'api_message': 'Update data berhasil',
        }

        return JsonResponse(response)

    except Exception as ex:
        response = {
            'error': str(ex),
            'status': ex.args
        }

        return JsonResponse(response)

