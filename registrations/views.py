from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Register
from .serializers import RegisterSerializer, LoginSerializer, ConfirmSerializer, ForgetSerializer, SentForgetSerializer, SearchSerializer
from email_app.views import send_email, send_forget_email
from log_app.views import create_log, update_log, delete_log, read_log
from django.contrib.auth.hashers import check_password, make_password, is_password_usable
import time

@api_view(['GET'])
def get_user(request, pk):
    token = request.META.get('HTTP_AUTHORIZATION','')
    get_token = Register.objects.get(token = token)
    if request.method == 'GET':
        registrations = Register.objects.get(pk=pk)
        serializer = SearchSerializer(registrations)    
        act = 'searching user id ' + str(pk)
        read_log(request,get_token,act)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT','DELETE'])
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
                    act = 'Read registrations by '
                    read_log(request,get_token,act)
                    return Response(serializer.data)

                elif request.method == 'DELETE':
                        act = 'Delete registrations within name : '
                        delete_log(request, get_token, get_token.full_name, act)
                        Register.delete()
                        content = {
                            'status' : 'NO CONTENT'
                        }
                        return Response(content, status=status.HTTP_202_NO_CONTENT)
                  
                elif request.method == 'PUT':                
                    serializer = RegisterSerializer(registrations, data=request.data)
                    if serializer.is_valid():
                        act = 'Update registrations by'
                        update_log(request, get_token, act)
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    
            except Register.DoesNotExist:
                    response = {'status': 'NAME NOT FOUND'}
                    return Response(response, status=status.HTTP_404_NOT_FOUND)
        
    except Register.DoesNotExist:
            content = {
                'status': 'Not Found'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def search(request):
    if request.method == 'POST':
        name = request.data['name']
        if (name == None) :
            network = Register.objects.all()
            serializer = RegisterSerializer(network, many=True)
            return Response(serializer.data)
        else:
            network = Register.objects.all().filter(full_name__icontains = name)
            serializer = RegisterSerializer(network, many=True)
            return Response(serializer.data)
            
@api_view(['GET', 'POST'])
def get_post_registrations(request):
    if request.method == 'GET':
        name = request.data['name']
        if (name == None) :
            network = Register.objects.all()
            serializer = RegisterSerializer(network, many=True)
            return Response(serializer.data)
        else:
            network = Register.objects.all().filter(full_name__icontains = name)
            serializer = RegisterSerializer(network, many=True)
            return Response(serializer.data)
    elif request.method == 'POST':        
        email_var = request.data['email']
        password = request.data['password'] 
        name = request.data['full_name']
        salt_password = ''.join(str(ord(c))for c in name)
        id_type = 0
        banned_type = "0"
        token = make_password(str(time.time()))
        hs_pass = make_password(str(password)+str(salt_password))
        payload ={
            'full_name' : name,
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
            'id_type' : id_type,
            'banned_type' : banned_type,
            'birth_day': request.data['birth_day'],
            'id_city' : request.data['id_city'],
            'token' : token
        }

        serializer = RegisterSerializer(data=payload)
        if serializer.is_valid():
            serializer.save()
            subjects = 'Activation account'
            try:
                send_email(request, email_var, token,name, subjects)
            except:
                return Response({'error in here'})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', 'GET'])
def get_login(request):
    if request.method == 'POST':
        email = request.data['email']
        key = request.data['password']
        salt = Register.objects.get(email=email).full_name
        salt_password = ''.join(str(ord(c)) for c in salt)
        password = key + salt_password
        token = make_password(str(time.time()))
        token_forget = 'usethistokenforforgetyourpassword'
        tokenx = str(token_forget) 
        try:
            get_login = Register.objects.get(email=email)
            if (check_password(tokenx, get_login.token)):
                response = {'status':'you request to change your password, please check your email'}
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)
            else:
                if (get_login.banned_type == "0"):
                    response = {'status':'Account has not verified yet, check your email to verified'}
                    return Response(response, status=status.HTTP_401_UNAUTHORIZED)
                else:                
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
                            act = 'user logging in by '
                            read_log(request, get_login, act)
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
                if (get_token.id == Registration):
                    get_out = {
                    'email': get_token.email,
                    'password': get_token.password,
                    'id_type': 0,
                    'token':'xxx'
                    }
                    serializer = LoginSerializer(get_token, data = get_out)
                    if serializer.is_valid():
                        act = 'user has logout by '
                        read_log(request, get_token, act)
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

@api_view(['POST'])
def verified_acc(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION')
        try:            
            get_token = Register.objects.get(token=token)
            payload = {
            'banned_type': "1"
            }
            serializer = ConfirmSerializer(get_token, data=payload)
            if serializer.is_valid():
                act = 'user has verified account with name : '
                read_log(request, get_token, act)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Register.DoesNotExist:
            response = {'status':'NOT FOUND'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def forget(request):
    if request.method == 'POST':
        token_forget = 'usethistokenforforgetyourpassword'
        tokenx = str(token_forget)
        token = make_password(tokenx)
        email = request.data['email']
        payload = {'token':token}
        try:
            check = Register.objects.get(email = email)
            name = check.full_name
            serializers = SentForgetSerializer(check, data = payload)
            if serializers.is_valid():
                serializers.save()
            else:
                return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
            subjects = 'Forget Password'
            send_forget_email(request, email, token, name, subjects)
            act = 'User requested to forget password by '
            read_log(request, check, act)
            return Response({'status':'Email sent'})
        except Register.DoesNotExist:
            response = {'status':'Email Does not valid'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def forget_backlink(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            get_token = Register.objects.get(token=token)
            token = make_password(str(time.time()))
            salt = get_token.full_name
            salt_password = ''.join(str(ord(c)) for c in salt)
            password = request.data['password'] 
            hs_pass = make_password(str(password)+str(salt_password))
            payload = {'password' : hs_pass, 'token':token}
            serializers = ForgetSerializer(get_token, data=payload)
            if serializers.is_valid():
                serializers.save()
                act = 'password is changed by '
                update_log(request, get_token, act)
                response = {'status':'Password chaged'}
                return Response(response, status=status.HTTP_201_CREATED)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        except Register.DoesNotExist:
            response = {'status': 'Your token is invalid'}
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
