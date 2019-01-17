from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Register
from .serializers import RegisterSerializer, LoginSerializer, ConfirmSerializer
from email_app.views import send_email
from django.contrib.auth.hashers import check_password, make_password, is_password_usable
import time

@api_view(['GET', 'PUT'])
def get_delete_update_registrations(request, pk):
    try:
        registrations = Register.objects.get(pk=pk)
        if (registrations.token == 'xxx'):
            response = {'status':'LOGIN FIRST, YOU MUST...'}
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        else:    
            try:
                token = request.META.get('HTTP_AUTHORIZATION','')
                get_token = Register.objects.get(token = token)                
            
                if request.method == 'GET':
                    serializer = RegisterSerializer(registrations)
                    return Response(serializer.data)

                elif request.method == 'DELETE':
                    
                        Register.delete()
                        content = {
                            'status' : 'NO CONTENT'
                        }
                        return Response(content, status=status.HTTP_202_NO_CONTENT)
                  
                elif request.method == 'PUT':                
                    serializer = RegisterSerializer(registrations, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    
            except Register.DoesNotExist:
                    response = {'status': 'UNAUTHORIZED'}
                    return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        
    except Register.DoesNotExist:
            content = {
                'status': 'Not Found'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def get_post_registrations(request):
    if request.method == 'GET':
        network = Register.objects.all()
        serializer = RegisterSerializer(network, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        salt_password = 'mindzzle'
        email_var = request.data['email']
        password = request.data['password'] 
        token = make_password(str(time.time()))
        hs_pass = make_password(str(password)+str(salt_password))
        payload ={
            'full_name' : request.data['full_name'],
            'email' : email_var,
            'salt_password' : salt_password,
            'password' : hs_pass,
            'primary_phone': request.data['primary_phone'],
            'primary_address' : request.data['primary_address'],
            'id_country' : request.data['id_country'],
            'id_regions' : request.data['id_regions'],
            'tax_num' : request.data['tax_num'],
            'url_photo' : request.data['url_photo'],
            'description' : request.data['description'],
            'id_type' : 0,
            'banned_type' : "0",
            'birth_day': request.data['birth_day'],
            'id_city' : request.data['id_city'],
            'token' : token
        }

        serializer = RegisterSerializer(data=payload)
        if serializer.is_valid():
            serializer.save()
            # send_email(email_var,token)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', 'GET'])
def get_login(request):
    if request.method == 'POST':
        email = request.data['email']
        key = request.data['password']
        salt_password = 'mindzzle'
        password = key + salt_password
        token = make_password(str(time.time()))
        try:
            get_login = Register.objects.get(email=email)
            if (get_login.banned_type == "0"):
                response = {'status':'Account has not verified yet, check your email to verified'}
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)
            else:                
                #is_password_usable(get_login.password)
                if (check_password(password, get_login.password)):                
                    get_in = {
                        'email': get_login.email,
                        'password': get_login.password,
                        'id_type': 1,
                        'banned_type':"1",
                        'token':token
                        }
                    serializer = LoginSerializer(get_login, data=get_in)
                    if serializer.is_valid():
                        serializer.save()
                        response = {
                        'status' : 'SUCCESSFULLY LOGIN',
                        'token' : get_login.token,
                        'id_user': get_login.id,
                        'email' : get_login.email
                        }                    
                        return Response(response, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    response = {'status' : 'Wrong Username / Password'}
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Register.DoesNotExist:
                response = {'status' : 'NOT Found'}
                return Response(response, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'GET':
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
            get_token = Register.objects.get(token = token)
            try:
                Registration = get_token.id
                # Registration = Register.objects.get(id=get_token.id)           
                if (get_token.id == Registration):
                    get_out = {
                    'email': get_token.email,
                    'password': get_token.password,
                    'id_type': 0,
                    'token':'xxx'
                    }
                    serializer = LoginSerializer(get_token, data = get_out)
                    if serializer.is_valid():
                        serializer.save()
                        response = {'status':'SUCCESSFULLY LOGOUT'}
                        return Response(response, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    response = {'status':'NOT FOUND 1'}
                    return Response(response, status=status.HTTP_404_NOT_FOUND)
            except Register.DoesNotExist:
                response = {'status':'NOT FOUND 2'}
                return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Register.DoesNotExist:
            response = {'status':'NOT FOUND 3'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
    else:
        response = {'status':'BAD REQUEST'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

# kelemahan system login yang ini. jika ada yang login selain kita. 
# maka token juga berubah.
@api_view(['POST'])
def verified_acc(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION')
        try:            
            get_token = Register.objects.get(token=token)
            payload = {
            # 'email':get_token.email,
            # 'password':get_token.password,
            # 'token': token,
            # 'id_type' : 0,
            'banned_type': "1"
            }
            serializer = ConfirmSerializer(get_token, data=payload)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Register.DoesNotExist:
            response = {'status':'NOT FOUND'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

# @api_view(['POST'])
# def verified_acc(request):
#     if request.method == 'POST':
#         email = request.data['email']
#         get_verified = Register.objects.get(email=email)
#         payload = {
#             'email' : email,
#             'password' : request.data['password'],
#             'banned_type' : 1
#             # 'token': make_password(str(time.time()))
#         }
#         serializer = LoginSerializer(get_verified, data=payload)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             response = {'status':'Wrong email / password'}
#             return Response(response, status=status.HTTP_400_BAD_REQUEST)

#     else:
#         response = {'status':'where are you going buddy?'}
#         return Response(response, status=status.HTTP_400_BAD_REQUEST)
