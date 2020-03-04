import datetime

from django.http import JsonResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from billing_license.models import BillingLicense
from billing_license.helper import _qty_license

from business_account.models import Business
from business_account.helper import _company_id

from email_app.views import reminder_email
from hierarchy.models import Hierarchy

from registrations.models import Register, Tokens
from registrations.helper import _cek_user


from .models import LicenseComp
from .serializers import LicenseCompSerializer, LicenseUpdateSerializer


@api_view(['GET'])
def search_all_div(request):
    try:
        beacon = LicenseComp.objects.all().values_list('id', flat=True)
        result = []
        for one in beacon:
            beaco = LicenseComp.objects.get(id=one)
            serializer = LicenseCompSerializer(beaco)
            dive = Hierarchy.objects.get(id=serializer.data['id_hierarchy'])
            user = Register.objects.get(id=dive.id_user)
            persona = {
                'id_user': user.id,
                'name': user.full_name
            }
            payload = {
                'division': dive.division,
                'data': serializer.data,
                'user': persona
            }
            result.append(payload)
        return Response(result, status=status.HTTP_201_CREATED)
    except LicenseComp.DoesNotExist:
        return Response({'status': 'License Company Does Not Exist'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'POST'])
def setting_license_company(request, pk):
    try:
        if request.method == 'POST':

            token = request.META.get('HTTP_AUTHORIZATION')
            user = Register.objects.get(token=token)
            company = Business.objects.get(id=pk, id_user=user.id)

            hierarchy_comp = Hierarchy.objects.all().values_list('id', flat=True).filter(id_company=company.id)
            result = []
            for inst in hierarchy_comp:
                payload = {
                    'id_hierarchy': inst,
                    'attendance': '0',
                    'payroll': '0',
                    'status': '0',
                    'id_comp': company.id
                }
                serializer = LicenseCompSerializer(data=payload)
                if serializer.is_valid():
                    serializer.save()
                    result.append(serializer.data)
            return Response(result, status=status.HTTP_201_CREATED)

        elif request.method == 'PUT':
            license_company = LicenseComp.objects.get(id=pk)
            serializer = LicenseCompSerializer(license_company, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'GET':
            try:

                beacon = LicenseComp.objects.all().values_list('id', flat=True).filter(id_comp=pk)
                result = []
                for one in beacon:
                    beaco = LicenseComp.objects.get(id=one)
                    serializer = LicenseCompSerializer(beaco)
                    dive = Hierarchy.objects.get(id=serializer.data['id_hierarchy'])
                    user = Register.objects.get(id=dive.id_user)
                    persona = {
                        'id_user': user.id,
                        'name': user.full_name
                    }
                    payload = {
                        'division': dive.division,
                        'data': serializer.data,
                        'user': persona
                    }
                    result.append(payload)
                return Response(result, status=status.HTTP_201_CREATED)
            except LicenseComp.DoesNotExist:
                return Response({'status': 'License Company Does Not Exist'}, status=status.HTTP_400_BAD_REQUEST)

    except Register.DoesNotExist:
        return Response({'status': 'User Does Not Exist'}, status=status.HTTP_404_NOT_FOUND)
    except Business.DoesNotExist:
        return Response({'status': 'Company Does Not Exist'}, status=status.HTTP_404_NOT_FOUND)
    except Hierarchy.DoesNotExist:
        return Response({'status': 'Hierarchy Does Not Exist'}, status=status.HTTP_400_BAD_REQUEST)
    except LicenseComp.DoesNotExist:
        return Response({'status': 'License Company Does Not Exist'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def reminder_exp_date(request):
    if request.method == 'GET':
        sekarang = datetime.datetime.now().date()
        resp = []
        comps = []
        beacon = LicenseComp.objects.all().values_list('expr_date', 'id_comp')
        for date, id_comp in beacon:
            if date == None:
                pass
            else:
                if date >= sekarang:
                    pass
                else:
                    if id_comp not in comps:
                        company = Business.objects.get(id=id_comp)
                        reminder_email(request, company)
                        res = {'Perusahaan :' + str(
                            company.company_name): 'masa waktu Lisensi anda telah habis, silahkan hubungi admin'}
                        resp.append(res)
                        comps.append(id_comp)
                    else:
                        pass
        return Response(resp)


@api_view(['GET'])
def license_company_views(request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION')
        _cek_token = Tokens.objects.filter(key=token).exists()
        if not _cek_token:
            response = {
                'api_status': status.HTTP_404_NOT_FOUND,
                'api_message': 'Anda telah logout sebelumnya'
            }

            return JsonResponse(response)

        _id_user = int(request.query_params['id_user'])
        _cek_id_user = Register.objects.filter(id=_id_user).exists()
        if not _cek_id_user:
            response = {
                'api_status': status.HTTP_404_NOT_FOUND,
                'api_message': 'User tidak terdaftar'
            }

            return JsonResponse(response)

        response = None
        if request.method == 'GET':
            _license_company = LicenseComp.objects.all().values_list('id', flat=True).\
                filter(id_comp=int(request.query_params['id_company']))

            result = []
            for i in _license_company:
                _license = LicenseComp.objects.get(id=i)

                user = Register.objects.get(id=_id_user)

                user_data = {
                    'id_user': user.id,
                    'name': user.full_name
                }

                _serializer = LicenseCompSerializer(_license)

                payload = {
                    'data': _serializer.data,
                    'user': user_data
                }

                result.append(payload)

                response = {
                    "api_status": status.HTTP_202_ACCEPTED,
                    "api_message": 'ambil data company berhasil',
                    'id_user': user.id,
                    "company": payload
                }

            return JsonResponse(response)
    except Exception as ex:
        response = {
            'error': str(ex),
            'status': ex.args
        }

        return JsonResponse(response)


@api_view(['GET', 'POST', 'PUT'])
def get_license_by_id_company(request):
    try:

        if request.method == 'GET':
            id_company = request.data['id_company']

            _data = BillingLicense.objects.filter(id_company=id_company).exists()
            if not _data:
                result = {
                    'api_status': status.HTTP_400_BAD_REQUEST,
                    'api_message': "Company belum memiliki license"
                }

                return JsonResponse(result)

            _qty = _qty_license(id_company)
            _company_id(id_company)
            _company = LicenseComp.objects.values_list('id', flat=True).filter(id_comp=id_company)
            result = []
            for c in _company:
                beaco = LicenseComp.objects.get(id=c)
                serializer = LicenseCompSerializer(beaco)
                _hierarchy = Hierarchy.objects.filter(id=serializer.data['id_hierarchy']).exists()
                dive = None
                if not _hierarchy:
                    continue
                elif _hierarchy:
                    dive = Hierarchy.objects.get(id=serializer.data['id_hierarchy'])
                user = Register.objects.get(id=dive.id_user)
                persona = {
                    'id_user': user.id,
                    'name': user.full_name
                }
                payload = {
                    'division': dive.division,
                    'data': serializer.data,
                    'user': persona
                }
                result.append(payload)

            response = {
                'api_status': status.HTTP_200_OK,
                'api_message': 'data employee menggunakan license',
                'expire_date_license': _qty.expire_date_license,
                'qty_license': _qty.qty_license,
                'data': result
            }

            return JsonResponse(response)
        elif request.method == 'POST':
            _company = _company_id(request.data['id_company'])
            _user = _cek_user(request.data['id_user'])

            hierarchy_comp = Hierarchy.objects.all().values_list('id', flat=True).filter(id_company=_company.id)
            result = []
            for comp in hierarchy_comp:
                payload = {
                    'id_hierarchy': comp,
                    'attendance': '0',
                    'payroll': '0',
                    'status': '0',
                    'id_comp': _company.id
                }
                serializer = LicenseCompSerializer(data=payload)
                if serializer.is_valid():
                    serializer.save()
                    result.append(serializer.data)

            response = {
                'api_status': status.HTTP_200_OK,
                'api_message': 'input license berhasil',
                'data': result
            }

            return JsonResponse(response)
        elif request.method == 'PUT':
            _company = _company_id(request.data['id_company'])
            _qty = _qty_license(_company.id)
            if _qty.qty_license == 0:
                response = {
                    'api_status': status.HTTP_400_BAD_REQUEST,
                    'api_message': 'Qty License anda sudah habis atau 0 license',
                }

                return JsonResponse(response)

            license_company = LicenseComp.objects.get(id_hierarchy=request.data['id_hierarchy'])

            payload = {
                "expr_date": _qty.expire_date_license,
                "status": '1'
            }

            serializer = LicenseUpdateSerializer(license_company, data=payload)
            if serializer.is_valid():
                serializer.save()

            response = {
                'api_status': status.HTTP_200_OK,
                'api_message': 'update license berhasil',
                'data': serializer.data
            }

            return JsonResponse(response)

    except Exception as ex:
        response = {
            'error': str(ex),
            'status': ex.args
        }

        return JsonResponse(response)

