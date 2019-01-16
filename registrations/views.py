from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Register
from .serializers import RegisterSerializer
from email_app.views import send_email
from django.contrib.auth.hashers import check_password, make_password, is_password_usable
import time

@api_view(['GET', 'PUT'])
def get_delete_update_registrations(request, pk):
    try:
        registrations = Register.objects.get(pk=pk)
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
                return Response(response, status=status.HTTP_404_NOT_FOUND)
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
            'id_type' : request.data['id_type'],
            'banned_type' : request.data['banned_type'],
            'birth_day': request.data['birth_day'],
            'id_city' : request.data['id_city'],
            'token' : token
        }

        serializer = RegisterSerializer(data=payload)
        if serializer.is_valid():
            serializer.save()
            send_email(email_var)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def get_login(request):
    if request.method == 'POST':
        email = request.data['email']
        key = request.data['password']
        salt_password = 'mindzzle'
        password = key + salt_password
        try:
            get_login = Register.objects.get(email=email)
            #is_password_usable(get_login.password)
            if (check_password(password, get_login.password)):
                response = {
                'status' : 'SUCCESSFULLY LOGIN',
                'token' : get_login.token,
                'id_user': get_login.id,
                'email' : get_login.email
                }
                return Response(response, status=status.HTTP_201_CREATED)
            else:
                response = {'status' : 'ERROR LOGIN'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Register.DoesNotExist:
                response = {'status' : 'NOT Found'}
                return Response(response, status=status.HTTP_404_NOT_FOUND)