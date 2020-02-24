import datetime

from django.http import JsonResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from business_account.models import Business
from email_app.views import reminder_email
from hierarchy.models import Hierarchy
from registrations.models import Register, Tokens


from .models import LicenseComp
from .serializers import LicenseCompSerializer


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




