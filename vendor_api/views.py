import csv
import datetime
import time
import logging
import requests
import json

from random import randint

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import EmailMessage
from django.http import HttpResponse

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from business_account.models import Business
from business_account.serializers import BusinessSerializer
from email_app.views import multidevices_email, vendors_login_alert
from hierarchy.models import Hierarchy
from hierarchy.serializers import HierarchySerializer
from join_company.models import Joincompany
from license_company.models import LicenseComp
from log_app.views import read_log
from registrations.models import Register
from registrations.serializers import forgetblastSerializer
from registrations.views import attempt_login, forget_attempt
from .models import Vendor_api, MultipleLogin
from .serializers import VendorSerializer, MultipleSerializer

logger = logging.info(settings.GET_LOGGER_NAME)

IsAdmin = "IsAdmin"
IsUser = "IsUser"
IsNothing = "IsNothing"


@api_view(['GET'])
def search_by_token(request, stri):
    try:
        token = request.META.get('HTTP_AUTHORIZATION')
        user = Register.objects.get(token=token)
        if stri == 'admincompany':
            admins = Business.objects.all().values_list('id', flat=True).filter(id_user=user.id)
            result = []
            for id_comp in admins:
                company = Business.objects.get(id=id_comp)
                payload = {
                    'id': company.id,
                    'name': company.company_name,
                    'logo': company.logo_path,
                    'parent_company': company.parent_company,
                    'email': company.email
                }
                result.append(payload)
            return Response(result, status=status.HTTP_200_OK)

        elif stri == 'usertoken':
            payload = {
                'id': user.id,
                'fullname': user.full_name,
                'token': user.token
            }
            return Response(payload, status=status.HTTP_200_OK)

        elif stri == 'join_company':
            joins = Joincompany.objects.all().values_list('id', flat=True).filter(id_user=user.id, status='2')
            result = []
            for join in joins:
                beacon = Joincompany.objects.get(id=join)
                payload = {
                    'id': beacon.id,
                    'id_company': beacon.id_company,
                    'id_rec': beacon.id_rec
                }
                result.append(payload)
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'The URL is Invalid, Please Check Again'}, status=status.HTTP_400_BAD_REQUEST)

    except Register.DoesNotExist:
        return Response({'status': 'Your Credential is Invalid, Please Login Again'},
                        status=status.HTTP_401_UNAUTHORIZED)
    except Business.DoesNotExist:
        return Response({'status': 'You are not an admin company'}, status=status.HTTP_401_UNAUTHORIZED)
    except Joincompany.DoesNotExist:
        return Response({'status': 'You dont have any employer'}, status=status.HTTP_200_OK)


# -----------------------------------------------BILLING API------------------------------------------------------------

@api_view(['GET'])
def sync_billing(request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION')
        admin = Register.objects.get(token=token)
        if admin.id != 0:
            return Response({'status': 'User Is Not Super Admin, Please contact Mindzzle Backend'},
                            status=status.HTTP_400_BAD_REQUEST)
        elif admin.id == 0:
            bisnis = Business.objects.all().values_list('id', 'id_user').filter(banned_type=2)
            result = []
            for id_biz, id_use in bisnis:
                beaconbiz = Business.objects.get(id=id_biz)
                bizser = BusinessSerializer(beaconbiz)
                bizadm = Register.objects.get(id=id_use)
                payload = {
                    'Business': bizser.data,
                    'Superadmin': {'name': bizadm.full_name, 'email': bizadm.email}
                }
                result.append(payload)
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'User did not have credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except Register.DoesNotExist:
        return Response({'status': 'User Did Not Exist'}, status=status.HTTP_404_NOT_FOUND)


# -----------------------------------------------PAYROLL API-----------------------------------------------------------------------------------
@api_view(['GET'])
def sync_emp_config(request):
    if request.method == 'GET':
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
            comp = request.data['comp_id']
            user = Register.objects.get(token=token)
            company = Business.objects.get(id_user=user.id, id=comp)
            hierarchy_comp = Hierarchy.objects.all().values_list('id', flat=True).filter(id_company=company.id)
            return Response({'result': hierarchy_comp}, status=status.HTTP_200_OK)
        except Register.DoesNotExist:
            return Response({'status': 'You Must Login First'}, status=status.HTTP_401_UNAUTHORIZED)
        except Business.DoesNotExist:
            return Response({'status': 'ID Company is Did not match'}, status=status.HTTP_404_NOT_FOUND)
        except Hierarchy.DoesNotExist:
            return Response({'status': 'Hierarchy is Empty, fill The company hierarchy first'})


@api_view(['GET'])
def check_hierarchy(request, pk):
    beacon = Hierarchy.objects.all().filter(id_company=pk)
    serializer = HierarchySerializer(beacon, many=True)
    return Response(serializer.data)


# @api_view(['GET'])
# def api_payroll(request, pk):
#     try:
#         _admins = Register.objects.get(id=pk)
#         comp = Business.objects.get(id=pk)
#         hierarki = Hierarchy.objects.get(id_company=pk, id_user=_admins.id)
#         license = LicenseComp.objects.get(id_comp=pk, status='1', id_hierarchy=hierarki.id)
#         if license.payroll == '2':
#             state = 'IsAdmin'
#             payload = {
#                 'status': state,
#                 'email': comp.email,
#                 'name': comp.company_name,
#                 'logo': comp.logo_path,
#             }
#             return Response(payload, status=status.HTTP_200_OK)
#
#         elif license.payroll == '1':
#             state = 'IsUser'
#         else:
#             state = 'IsNothing'
#
#         payload = {
#             'status': state,
#             'id_comp': pk
#         }
#         return Response(payload, status=status.HTTP_200_OK)
#     except Register.DoesNotExist:
#         return Response({'status': 'User is not exist.'}, status=status.HTTP_401_UNAUTHORIZED)
#     except Business.DoesNotExist:
#         return Response({'status': 'User is not admin company.'}, status=status.HTTP_401_UNAUTHORIZED)
#     except Hierarchy.DoesNotExist:
#         return Response({'status': 'User is not in Hierarchy company.'}, status=status.HTTP_401_UNAUTHORIZED)
#     except LicenseComp.DoesNotExist:
#         return Response({'status': 'User is not Registered in License company.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["GET", "POST"])
def get_data_payroll(request):
    """
    get data employee for setting company
    :param request: id_user, id_company, token
    :return: json data company by id_company
        {
            "status": "IsAdmin",
            "email": "testig12@gmail.com",
            "name": "testing12",
            "logo": ""
        }
    """
    try:
        if request.method == "GET":
            _token = Register.objects.filter(token=request.query_params['token_user']).exists()
            if not _token:
                return Response({'status': 'User Token, is Unauthorized.'},
                                status=status.HTTP_401_UNAUTHORIZED)

            _user = Register.objects.get(id=request.query_params['id_user'])
            if not _user:
                return Response({'status': 'User is not exist.'},
                                status=status.HTTP_401_UNAUTHORIZED)

            _comp = Business.objects.get(id=request.query_params['id_company'])
            if not _comp:
                return Response({'status': 'User is not admin company.'},
                                status=status.HTTP_401_UNAUTHORIZED)

            _hierarchy = Hierarchy.objects.get(id_company=_comp.id, id_user=_user.id)
            if not _hierarchy:
                return Response({'status': 'User is not in Hierarchy company.'},
                                status=status.HTTP_401_UNAUTHORIZED)

            _license = LicenseComp.objects.get(id_comp=_comp.id, status='1', id_hierarchy=_hierarchy.id)
            if not _license:
                return Response({'status': 'User is not Registered in License company.'},
                                status=status.HTTP_401_UNAUTHORIZED)

            if _license.payroll == '2':
                state = IsAdmin
                payload = {
                    'status': state,
                    "id_comp": _comp.id,
                    'email': _comp.email,
                    'name': _comp.company_name,
                    'logo': _comp.logo_path,
                }

                response = HttpResponse(json.dumps(payload), content_type="application/json")
                return response

            elif _license.payroll == '1':
                state = IsUser
            else:
                state = IsNothing

            payload = {
                'status': state,
                'id_comp': _comp.id
            }
            return Response(payload, status=status.HTTP_200_OK)

        elif request.method == "POST":
            _token = Register.objects.filter(token=request.data['token_user']).exists()
            if not _token:
                return Response({'status': 'User Token, is Unauthorized.'},
                                status=status.HTTP_401_UNAUTHORIZED)

            _user = Register.objects.get(id=request.data['id_user'])
            if not _user:
                return Response({'status': 'User is not exist.'},
                                status=status.HTTP_401_UNAUTHORIZED)

            _comp = Business.objects.get(id=request.data['id_company'])
            if not _comp:
                return Response({'status': 'User is not admin company.'},
                                status=status.HTTP_401_UNAUTHORIZED)

            payload = {
                'id_user': _user.id,
                'id_company': _comp.id,
                'company_name': _comp.company_name
            }
            response = HttpResponse(json.dumps(payload), content_type="application/json")
            return response

    except Exception as ex:
        logger.error({
            'errorType': 500,
            'message': ex.args[0]
        })


# -----------------------------------------------------REGISTER THIRD PARTY API------------------------------------------------------------------
@api_view(['GET', 'POST', 'DELETE'])
def generate(request):
    if request.method == 'POST':
        # jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        # jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        vendor = request.data['vendors']
        username = request.data['username']
        password = request.data['password']
        hashes = ''.join(str(ord(c)) for c in vendor)

        # payload = jwt_payload_handler(username)
        # token = jwt_encode_handler(payload)
        # token = request.data['token']

        payloads = {
            'username': username,
            'password': make_password(str(hashes) + str(password)),
            'vendor_name': vendor,
            'token': make_password(str(hashes) + 'Mind55L3')
        }
        serializer = VendorSerializer(data=payloads)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            user = Register.objects.get(token=token)
            if user.id == 0:
                comp_token = request.data['token_comp']
                comp = Vendor_api.objects.get(token=comp_token)
                comp.delete()
                return Response({'status': 'Deleted'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'status': 'Hold up, you are not authorized to access this'},
                                status=status.HTTP_401_UNAUTHORIZED)
        except Vendor_api.DoesNotExist:
            return Response({'status': 'Vendor Not Found'}, status=status.HTTP_404_NOT_FOUND)
        except Register.DoesNotExist:
            return Response({'status': 'YOU DONT HAVE ACCESS.'}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
            user = Register.objects.get(token=token)
            if user.id == 0:
                network = Vendor_api.objects.all()
                serializer = VendorSerializer(network, many=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'status': 'YOU DONT HAVE ACCESS'}, status=status.HTTP_401_UNAUTHORIZED)
        except Register.DoesNotExist:
            return Response({'status': 'YOU ARE NOTHING.'}, status=status.HTTP_400_BAD_REQUEST)


# ------------------------------------------------GENERAL API--------------------------------------------------------------------------------------------
@api_view(['GET', 'POST'])
def login_logout_vendors(request):
    if request.method == 'POST':
        try:
            username = request.data['username']
            password = request.data['password']
            beacon = Vendor_api.objects.get(username=username)
            hashes = ''.join(str(ord(c)) for c in beacon.vendor_name)
            key = hashes + password
            if (check_password(key, beacon.password)):
                payloads = {
                    'username': username,
                    'password': make_password(str(hashes) + str(password)),
                    'vendor_name': beacon.vendor_name,
                    'token': make_password(str(hashes) + 'Mind55L3')
                }
                serializer = VendorSerializer(beacon, data=payloads)
                if serializer.is_valid():
                    serializer.save()
                    vendors = serializer.data['vendor_name']
                    vendors_login_alert(request, vendors)
                    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'status': 'wrong username / password'}, status=status.HTTP_401_UNAUTHORIZED)
        except Vendor_api.DoesNotExist:
            return Response({'status': 'YOU DONT HAVE ACCESS.'}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
            beacon = Vendor_api.objects.get(token=token)
            payload = {
                'username': beacon.username,
                'password': beacon.password,
                'vendor_name': beacon.vendor_name,
                'token': 'xxx'
            }
            serializer = VendorSerializer(beacon, data=payload)
            if serializer.is_valid():
                serializer.save()
                vendors = beacon.vendor_name
                vendors_login_alert(request, vendors)
                return Response({'status': 'YOU HAS LOGOUT'}, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Vendor_api.DoesNotExist:
            return Response({'status': 'YOU MOST LOGIN FIRST.'}, status=status.HTTP_401_UNAUTHORIZED)


def ERP_token_generator():
    range_start = 10 ** (6 - 1)
    range_end = (10 ** 6) - 1
    return randint(range_start, range_end)


@api_view(['POST', 'PUT', 'GET'])
def api_login_absensee_v2(request, pk):
    try:
        if request.method == 'POST':
            token_vendor = request.META.get('HTTP_AUTHORIZATION')
            if token_vendor == 'xxx':
                return Response({'status': 'Vendor Token, is Unauthorized.'}, status=status.HTTP_401_UNAUTHORIZED)
            vendor = Vendor_api.objects.get(token=token_vendor)

            email = request.data['email']
            password = request.data['password']

            # ------------------tambahan ----------------------
            # token = request.META.get('HTTP_AUTHORIZATION')
            user = Register.objects.get(email=email)
            comp = Business.objects.get(id_user=user.id, id=pk)
            hierarki = Hierarchy.objects.get(id_company=comp.id, id_user=user.id)
            license = LicenseComp.objects.get(id_comp=comp.id, status='1', id_hierarchy=hierarki.id)
            sekarang = datetime.datetime.now().date()

            if datetime.datetime.strptime(str(license.expr_date), '%Y-%m-%d').date() >= sekarang:
                masa = 'Masih bisa'
            else:
                return Response({'status': 'udah expired'}, status=status.HTTP_401_UNAUTHORIZED)

            if vendor.username == 'Absensee':
                if license.attendance == '2':
                    state = 'IsAdmin'
                elif license.attendance == '1':
                    state = 'IsUser'
                else:
                    state = 'IsNothing'

            elif vendor.username == 'Billing':
                if license.billing == '2':
                    state = 'IsAdmin'
                elif license.billing == '1':
                    state = 'IsUser'
                return Response({'status': state}, status=status.HTTP_200_OK)

            elif vendor.username == 'ERP':
                if license.attendance == '2':
                    state = 'IsAdmin'
                elif license.attendance == '1':
                    state = 'IsUser'
                else:
                    return Response({'status': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

                token = ERP_token_generator()

                # payload = {
                # 'id_user':user.id,
                # 'name':user.full_name,
                # 'state':state,
                # 'token':token
                # }

                if settings.FLAG == 0:
                    url = 'http://dev-erp-api.mindzzle.com/login/savetoken/'
                elif settings.FLAG == 1:
                    url = 'https://erp-api.mindzzle.com/login/savetoken/'
                elif settings.FLAG == 3:
                    url = 'http://127.0.0.1:8088/login/savetoken/'

                payload_erp = {
                    'id_user': user.id,
                    'username': user.full_name,
                    'token': token
                }

                Req = requests.post(url + str(user.id), data=payload_erp)
                Res = Req.json()

                return Response(Res, status=status.HTTP_200_OK)

            elif vendor.username == 'payroll':
                if license.payroll == '2':
                    state = 'IsAdmin'
                elif license.payroll == '1':
                    state = 'IsUser'
                else:
                    state = 'IsNothing'

                payload = {
                    'token': user.token,
                    'status': state,
                    'id_comp': comp.id,
                    'masa': masa
                }
                act = "this user accessing Payroll app"
                read_log(request, user, act)
                return Response(payload, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'Vendor Belum Terintegrasi Dengan Mindzzle'})
            # ---------------------------------------------------------

            # user = Register.objects.get(email = email)
            multiple_login = MultipleLogin.objects.get(id_user=user.id)
            # -------------------only single phone-------------------
            if multiple_login.token_phone != 'xxx':
                return Response({'status': 'You Have Login In Multiple Phone Devices, Please Logout first'},
                                status=status.HTTP_401_UNAUTHORIZED)
            # -------------------------------------------------------
            attempt = user.attempt
            salt = user.full_name
            salt_password = ''.join(str(ord(c)) for c in salt)
            thepassword = password + salt_password

            if (check_password(thepassword, user.password)):
                token = make_password(str(time.time()))
                payload = {
                    'id_user': user.id,
                    'token_web': user.token,
                    'token_phone': token
                }
                serializer = MultipleSerializer(multiple_login, data=payload)
                # ----------------------TESTING (tambahan v2)----------------------
                if serializer.is_valid():
                    serializer.save()
                    beacon = Business.objects.get(id=pk)
                    payload = {
                        'token_user': user.token,
                        'image': beacon.logo_path,
                        'comp_id': beacon.id,
                        'comp_name': beacon.company_name,
                        'masa': masa
                    }
                    act = "this user accessing " + vendor.username + " app"
                    read_log(request, user, act)
                    multidevices_email(request, user)
                    return Response(payload, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # ---------------------------------------------------

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
            user = Register.objects.get(token=token)
            if user.id == 0:
                migrates = Register.objects.all().values_list('id', 'token').filter(verfied=1)
                result = []
                for id_user, token in migrates:
                    payload = {
                        'id_user': id_user,
                        'token_web': token,
                        'token_phone': 'xxx'
                    }
                    serializer = MultipleSerializer(data=payload)
                    if serializer.is_valid():
                        serializer.save()
                        result.append(serializer.data)
                return Response({'status': result}, status=status.HTTP_201_CREATED)
            return Response({'status': 'You Do Not Have Super Admin Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        elif request.method == 'PUT':
            token_vendor = request.META.get('HTTP_AUTHORIZATION')
            token_user = request.data['token_user']
            vendor = Vendor_api.objects.get(token=token_vendor)
            user = Register.objects.get(token=token_user)
            multiple_login = MultipleLogin.objects.get(id_user=user.id)
            payload = {
                'id_user': user.id,
                'token_web': user.token,
                'token_phone': 'xxx'}
            serializer = MultipleSerializer(multiple_login, data=payload)
            if serializer.is_valid():
                serializer.save()
                act = "this user Logout " + vendor.username + " app"
                read_log(request, user, act)
                return Response({'status': 'User Has Logout'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Vendor_api.DoesNotExist:
        return Response({'status': 'Vendor Token, is Does Not Exist.'}, status=status.HTTP_401_UNAUTHORIZED)
    except Register.DoesNotExist:
        return Response({'status': 'User is Unauthorized.'}, status=status.HTTP_401_UNAUTHORIZED)
    except Joincompany.DoesNotExist:
        return Response({'status': 'User did not have any company'}, status=status.HTTP_202_ACCEPTED)
    except Business.DoesNotExist:
        return Response({'status': 'The Company Does Not Exist'}, status=status.HTTP_202_ACCEPTED)
    except Hierarchy.DoesNotExist:
        return Response({'status': 'User is not in Hierarchy company.'}, status=status.HTTP_401_UNAUTHORIZED)
    except LicenseComp.DoesNotExist:
        return Response({'status': 'User is not Registered in License company.'}, status=status.HTTP_401_UNAUTHORIZED)
    except MultipleLogin.DoesNotExist:
        return Response({'status': 'User is not Registered in multiple devices.'}, status=status.HTTP_401_UNAUTHORIZED)


# ---------------------------------------ATTENDANCE API------------------------------------------------------------------------------------
@api_view(['POST', 'PUT'])
def api_login_absensee(request):
    try:
        token_vendor = request.META.get('HTTP_AUTHORIZATION')
        if token_vendor == 'xxx':
            return Response({
                'status': 'Vendor Token, is Unauthorized.'}, status=status.HTTP_401_UNAUTHORIZED)

        # check method
        if request.method == 'POST':
            email = request.data['email']
            password = request.data['password']

            user = Register.objects.get(email=email)
            full_name = user.full_name
            salt_password = ''.join(str(ord(c)) for c in full_name)
            _password = password + salt_password

            # check login
            if check_password(_password, user.password):
                token = make_password(str(time.time()))

                multiple_login = MultipleLogin.objects.get(id_user=user.id)

                # check condition if token phone already login at another phone
                if multiple_login.token_phone != "xxx":
                    payloads = {
                        'id_user': user.id,
                        'token_web': user.token,
                        'token_phone': "xxx"
                    }

                    _del_token_phone = MultipleSerializer(multiple_login, data=payloads)
                    if _del_token_phone.is_valid():
                        _del_token_phone.save()

                payload = {
                    'id_user': user.id,
                    'token_web': user.token,
                    'token_phone': token
                }

                serializer = MultipleSerializer(multiple_login, data=payload)

                if serializer.is_valid():
                    serializer.save()
                    profil = {
                        'id': user.id,
                        'name': user.full_name,
                        'photo': user.url_photo
                    }

                    payloads = {
                        'api_status': 1,
                        'api_message': 'success',
                        'profile': profil,
                    }

                    return Response(payloads, status=status.HTTP_201_CREATED)

                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                attempt_login(request, email)
                response = {'status': 'Wrong Username / Password'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'PUT':
            token_user = request.data['token_user']
            multiple_login = MultipleLogin.objects.get(token_phone=token_user)
            user = Register.objects.get(id=multiple_login.id_user)
            payload = {
                'id_user': user.id,
                'token_web': user.token,
                'token_phone': 'xxx'}
            serializer = MultipleSerializer(multiple_login, data=payload)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'User Has Logout'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Vendor_api.DoesNotExist:
        return Response({'status': 'Vendor Token, is Unauthorized.'}, status=status.HTTP_401_UNAUTHORIZED)
    except Register.DoesNotExist:
        return Response({'status': 'Wrong Username / Password'}, status=status.HTTP_401_UNAUTHORIZED)
    except Joincompany.DoesNotExist:
        return Response({'status': 'User did not have any company'}, status=status.HTTP_202_ACCEPTED)
    except Business.DoesNotExist:
        return Response({'status': 'The Company Does Not Exist'}, status=status.HTTP_202_ACCEPTED)
    # except LicenseComp.DoesNotExist:
    # 	return Response({'stat':hirarki.id,'status':'User is not Registered in License company.'}, status = status.HTTP_401_UNAUTHORIZED)
    # except Hierarchy.DoesNotExist:
    # 	return Response({'status':'Hierarchy does not exist.'}, status = status.HTTP_401_UNAUTHORIZED)
    except MultipleLogin.DoesNotExist:
        return Response({'status': 'User is not Registered in multiple devices.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def logout_by_email(request):
    if request.method == 'GET':
        if settings.FLAG == 0:
            url = 'http://dev-user-api.mindzzle.com/vendor/api/api_login_absensee/'
        elif settings.FLAG == 1:
            url = 'https://x-user-api.mindzzle.com/vendor/api/api_login_absensee/'
        elif settings.FLAG == 2:
            url = 'http://staging-user-api.mindzzle.com/vendor/api/api_login_absensee/'
        elif settings.FLAG == 3:
            url = 'http://127.0.0.1:8000/vendor/api/api_login_absensee/'

        header = {'Authorization': 'pbkdf2_sha256$120000$I2BCKb0Nflgy$96qeihph6v7Ibpy4st7u5WAFBIRxOUKxHB28r8NlM5U='}
        token = request.query_params.get('token')
        payload = {'token_user': token}
        req = requests.put(url, headers=header, data=payload)
        res = req.json()
        return Response(res, status=status.HTTP_200_OK)


@api_view(['GET'])
def migrate_multiuser_company(request, pk):
    try:
        result = []
        token = request.META.get('HTTP_AUTHORIZATION')
        suser = Register.objects.get(token=token)
        if suser.id == 0:
            join = Joincompany.objects.all().values_list('id_user', flat=True).filter(id_company=pk, status='2')

            for id_user in join:
                user = Register.objects.get(id=id_user)
                try:
                    hirarki = Hierarchy.objects.get(id_user=id_user, id_company=pk)
                    license = LicenseComp.objects.get(id_hierarchy=hirarki.id)
                    if license.attendance == '0':
                        payload = {
                            'id_user': user.id,
                            'name': 'Your Attendance Is Not Active',
                            'photo': 'Your Attendance Is Not Active'
                        }
                        result.append(payload)
                        pass
                    # return Response({'status':'Your Attendance is not Active'}, status = status.HTTP_401_UNAUTHORIZED)
                    payload = {
                        'id_user': user.id,
                        'name': user.full_name,
                        'photo': user.url_photo
                    }
                    serializer = MultipleSerializer(data=payload)
                    if serializer.is_valid():
                        try:
                            serializer.save()
                            rest = serializer.data
                            result.append(rest)
                        except Exception:
                            pass
                            rest = serializer.errors
                            result.append(rest)
                except Hierarchy.DoesNotExist:
                    payload = {
                        'id_user': user.id,
                        'name': 'Your id is not attached in Company Hierarcy',
                        'photo': 'Your id is not attached in Company Hierarcy'
                    }
                    result.append(payload)
                    pass
                except LicenseComp.DoesNotExist:
                    payload = {
                        'id_user': user.id,
                        'name': 'Your id is not attached in License Company ',
                        'photo': 'Your id is not attached in License Company'
                    }
                    result.append(payload)
                    pass
                # return Response({'status':str(user.id)+' Hierarchy Does Not Exist'}, status = status.HTTP_401_UNAUTHORIZED)
            return Response({'status': result}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'You Are Not Super User'}, status=status.HTTP_401_UNAUTHORIZED)
    except Register.DoesNotExist:
        return Response({'status': 'Token is Invalid'}, status=status.HTTP_401_UNAUTHORIZED)
    # except LicenseComp.DoesNotExist:
    # 	return Response({'status':'Your License is not Active'}, status = status.HTTP_401_UNAUTHORIZED)
    # except Hierarchy.DoesNotExist:
    # 	return Response({'status':'Hierarchy Does Not Exist'}, status = status.HTTP_401_UNAUTHORIZED)
    except Joincompany.DoesNotExist:
        return Response({'status': 'Your Attendance is not Active'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def check_token(request):
    if request.method == 'GET':
        try:
            token_ven = request.META.get('HTTP_AUTHORIZATION')
            tokenhp = request.data['token_user']
            beaconhp = MultipleLogin.objects.get(token_phone=tokenhp)
            token = beaconhp.token_web
            beacon_vendor = Vendor_api.objects.get(token=token_ven)
            beacon = Register.objects.get(token=token)
            return Response({'status': 'Okay', 'token': beacon.token, 'id': beacon.id}, status=status.HTTP_200_OK)
        except Vendor_api.DoesNotExist:
            return Response({'status': 'Vendor Token, is Unauthorized.'}, status=status.HTTP_401_UNAUTHORIZED)
        except Register.DoesNotExist:
            return Response({'status': 'User Token, is Unauthorized.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def check_admin_attendace(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            vendor = Vendor_api.objects.get(token=token)
            tokenhp = request.data['token_user']
            # beacon = MultipleLogin.objects.get(token_web = tokenhp)
            # token_user = beacon.token_web
            id_comp = request.data['id_company']
            user = Register.objects.get(token=tokenhp)
            company = Business.objects.get(id=id_comp)
            hirarki = Hierarchy.objects.get(id_user=user.id, id_company=company.id)
            license_comp = LicenseComp.objects.get(id_comp=id_comp, status='1', id_hierarchy=hirarki.id)
            if license_comp.attendance == '1':
                return Response({'status': 'User is not Admin'}, status=status.HTTP_401_UNAUTHORIZED)
            elif license_comp.attendance == '2':
                persona = {
                    'id': user.id,
                    'name': user.full_name
                }

                bisnis = {
                    'id': company.id,
                    'name': company.company_name
                }
                payload = {
                    'status': 'IsAdmin',
                    'User': persona,
                    'Company': bisnis
                }
                return Response(payload, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'User is unauthorized at all in this page'},
                                status=status.HTTP_401_UNAUTHORIZED)
        except Vendor_api.DoesNotExist:
            return Response({'status': 'Vendor Token, is Unauthorized.'}, status=status.HTTP_401_UNAUTHORIZED)
        except Register.DoesNotExist:
            return Response({'status': 'User token is Invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        except Business.DoesNotExist:
            return Response({'status': 'The Company Does Not Exist'}, status=status.HTTP_202_ACCEPTED)
        except LicenseComp.DoesNotExist:
            return Response({'stat': hirarki.id, 'status': 'User is not Registered in License company.'},
                            status=status.HTTP_401_UNAUTHORIZED)
        except Hierarchy.DoesNotExist:
            return Response({'status': 'Hierarchy does not exist.'}, status=status.HTTP_401_UNAUTHORIZED)
        except MultipleLogin.DoesNotExist:
            return Response({'stat': hirarki.id, 'status': 'Multiple Login does not exist.'},
                            status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def get_data_employee(request):
    """
    function for get all data base on id_company
    :param request: id_company
    :return: data all employee
    """
    try:
        _token = request.META.get('HTTP_AUTHORIZATION')
        _vendor = Vendor_api.objects.get(token=_token)
        if not _vendor:
            return Response({
                'status': 'Vendor Token, is Unauthorized.'}, status=status.HTTP_401_UNAUTHORIZED)

        _id_comp = request.data['id_company']
        _company_data = Business.objects.filter(id=_id_comp).exists()
        if not _company_data:
            return Response({'status': 'The Company Does Not Exist'}, status=status.HTTP_202_ACCEPTED)

        _hirarki = Hierarchy.objects.all().values_list('id', flat=True).filter(id_company=_id_comp)
        if not _hirarki:
            return Response({'status': 'Hierarchy does not exist.'}, status=status.HTTP_401_UNAUTHORIZED)

        result = []
        for hirarki in _hirarki:
            _id_hirarki = Hierarchy.objects.get(id=hirarki)
            if _id_hirarki.id_user == 0:
                pass
            else:
                _user = Register.objects.get(id=_id_hirarki.id_user)
                _license = LicenseComp.objects.filter(id_hierarchy=_id_hirarki.id).first()

                if _license is None:
                    level = 'User / Company Belum Mengaktifkan Fitur Ini'
                elif _license.attendance == '2':
                    level = IsAdmin
                else:
                    level = IsUser

                payload = {
                    'id': _user.id,
                    'fullname': _user.full_name,
                    'photo': _user.url_photo,
                    'email': _user.email,
                    'level': level
                }

                result.append(payload)

        _id_comp = request.data['id_company']
        company = Business.objects.get(id=_id_comp)
        payloads = {
            'company_id': company.id,
            'company_name': company.company_name,
            'logo': company.logo_path,
            'employees': result
        }
        return Response(payloads, status=status.HTTP_200_OK)

    except Exception as ex:
        logger.error({
            'errorType': 500,
            'message': ex.args
        })


@api_view(['GET'])
def timesheets_absensee(request):
    if settings.FLAG == 0:
        url = 'http://dev-attandance.mindzzle.com/api/timesheets'
    elif settings.FLAG == 1:
        url = 'https://x-attandance.mindzzle.com/api/timesheets'

    Req = requests.get(url)
    Res = Req.json()
    return Response(Res, status=status.HTTP_200_OK)


@api_view(['GET'])
def api_find_company_absensee(request):
    try:
        token_vendor = request.META.get('HTTP_AUTHORIZATION')
        vendor = Vendor_api.objects.get(token=token_vendor)
        tokenhp = request.data['token_user']
        beacon = MultipleLogin.objects.get(token_phone=tokenhp)
        token = beacon.token_web
        id_comp = request.data['id_comp']
        user = Register.objects.get(token=token)
        company = Business.objects.get(id=id_comp)
        hierarchy = Hierarchy.objects.get(id_user=user.id, id_company=id_comp)
        license = LicenseComp.objects.get(id_hierarchy=hierarchy.id, id_comp=hierarchy.id_company)
        if license.attendance == '1':
            auth = 'IsUser'
        elif license.attendance == '2':
            auth = 'IsAdmin'
        else:
            return Response({'status': 'User is Unauthorized to Attendance.'}, status=status.HTTP_401_UNAUTHORIZED)
        payload = {
            'fullname': user.full_name,
            'division': hierarchy.division,
            'company_name': company.company_name,
            'client_auth': auth,
            'client_token': user.token
        }
        return Response(payload, status=status.HTTP_202_ACCEPTED)
    except Vendor_api.DoesNotExist:
        return Response({'status': 'Vendor Token, is Unauthorized.'}, status=status.HTTP_401_UNAUTHORIZED)
    except Register.DoesNotExist:
        return Response({'status': 'User is Unauthorized.'}, status=status.HTTP_401_UNAUTHORIZED)
    except Hierarchy.DoesNotExist:
        return Response({'status': 'User did not have any relation in the company'}, status=status.HTTP_202_ACCEPTED)
    except Business.DoesNotExist:
        return Response({'status': 'The Company Does Not Exist'}, status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
def email_forget_blast(request):
    # awal = request.data['awal']
    # akhir = request.data['akhir']
    emails = request.FILES['list_email']
    # df = pd.read_excel(emails)
    email = df['email']

    respon = []
    # for eml in range(0,len(email)):
    # 	email = email[eml]
    for email in emails:
        try:
            user = Register.objects.get(email=email)
            key = 'Jeera1234' + user.salt_password
            token_forget = 'usethistokenforforgetyourpassword'
            if check_password(key, user.password):
                if user.banned_type != '0':
                    url = 'https://user-api.mindzzle.com/registrations/api/forget/'
                    payload = {
                        'email': user.email
                    }
                    Req = requests.post(url, data=payload)
                    Res = Req.json()
                    respon.append(payload)
                else:
                    serializer = forgetblastSerializer(user, data={'banned_type': '1', 'verified': 1})
                    if serializer.is_valid():
                        serializer.save()
                        respon.append(str(user.id) + '. ' + email + ' : Get Banned')
                    else:
                        respon.append(serializer.errors)
                        pass
            elif check_password(token_forget, user.password):
                if user.banned_type != '0':
                    respon.append(str(user.id) + '. ' + email + ' : Has Forget their password')
                else:
                    serializer = forgetblastSerializer(user, data={'banned_type': '1', 'verified': 1})
                    if serializer.is_valid():
                        serializer.save()
                        respon.append(str(user.id) + '. ' + email + ' : Has Forget their password And Get Banned')
                    else:
                        respon.append(serializer.errors)
                pass
            else:
                if user.banned_type != '0':
                    respon.append(str(user.id) + '. ' + email + ' : Password Has Changed')
                else:
                    serializer = forgetblastSerializer(user, data={'banned_type': '1', 'verified': 1})
                    if serializer.is_valid():
                        serializer.save()
                        respon.append(str(user.id) + '. ' + email + ' : Password Has Changed But Get banned')
                    else:
                        respon.append(serializer.errors)
                pass
        except Register.DoesNotExist:
            respon.append(email + ' : does not exist')
            pass
        # return Response({'status':'User Not Found'}, status = status.HTTP_404_NOT_FOUND)
    return Response(respon, status=status.HTTP_200_OK)


# else:
# 	return Response({'status':'Unauthorized'}, status = status.HTTP_401_UNAUTHORIZED)


# @api_view(['GET'])
# def email_blast(request):
# 	awal = request.data['awal']
# 	akhir  = request.data['akhir']
# 	respon = []
# 	try:
# 		for id_user in range(int(awal), int(akhir)):
# 			user = Register.objects.get(id = id_user)

@api_view(['POST'])
def send_blast(request):
    if request.method == 'POST':
        awal = request.data['awal']
        akhir = request.data['akhir']
        result = []
        try:
            for id_user in range(int(awal), int(akhir)):
                # #--------------DATA---------------------
                user = Register.objects.get(id=id_user)
                recipient = user.email
                msg = EmailMessage(
                    'Info Mobile Apps Mindzzle',
                    'Silahkan Untuk Download aplikasi Mindzzle dengan link dibawah ini \n Android : https://play.google.com/store/apps/details?id=com.reprime.mindzzle.attendance \n IOS : https://apps.apple.com/id/app/mindzzle-attendance/id1463349473',
                    'admin@mindzzle.com',
                    [recipient],
                )
                # try:
                msg.send()
                sre = {'status': str(user.email) + ' Berhasil Dikirim'}
                result.append(sre)
                # except Exception:
                #     sre ={'status':str(user.email)+' Gagal Dikirim'}
                #     result.append(sre)
        except Register.DoesNotExist:
            pass
        return Response(result)


@api_view(['GET'])
def download_data(request):
    items = MultipleLogin.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename = "multiplelogin.csv"'

    writer = csv.writer(response, delimiter=',')
    writer.writerow(['id_user', 'token_web', 'token_phone'])

    for obj in items:
        writer.writerow([obj.id_user, obj.token_web, obj.token_phone])

    return response


@api_view(['GET'])
def employee_cred(request):
    id_comp = request.data['id_comp']
    result = []
    try:
        beacon = Hierarchy.objects.all().values_list('id_user', 'division').filter(id_company=id_comp)
        comp = Business.objects.get(id=id_comp)
        for userId, div in beacon:
            try:
                user = Register.objects.get(id=userId).full_name
                # dalaman = {'division':div, 'name':user}
                if userId == 0:
                    pass
                else:
                    hasil = {'id_user': userId, 'division': div, 'name': user, 'comp_name': comp.company_name}
                    result.append(hasil)
            except Register.DoesNotExist:
                resp = 'user ' + userId + ' does not exist'
                result.append(resp)
                pass
        return Response(result)
    except Business.DoesNotExist:
        return Response({'status': 'id company does not match !'})
    except Hierarchy.DoesNotExist:
        return Response({'status': 'Hierarchy Company does not exist !'})
