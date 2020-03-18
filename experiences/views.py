from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from business_account.models import Business
from log_app.views import read_log, update_log, delete_log
from registrations.models import Register
from registrations.authentication import is_authentication

from .models import Experiences as pengalaman
from .serializers import ExperiencesSerializer


@api_view(['GET','DELETE', 'PUT'])
def get_delete_update_experiences(request, pk):
    if request.method == 'DELETE':
        Experiences = pengalaman.objects.get(id=pk)
        registrations = Register.objects.get(id=Experiences.id_user)
        if (Experiences.verified == "0"):                    
            Experiences.delete()
            act = 'Delete experience by id : '                           
            delete_log(request, registrations, Experiences.position, act)
            content = {
                'status' : 'NO CONTENT'
            }
            return Response(content, status=status.HTTP_204_NO_CONTENT)
        else:
            content = {'status':'Cannot touch this, because your experience already verified'}
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)
    else:
        try:
            Experiences = pengalaman.objects.get(id=pk)
            company = Business.objects.get(id = Experiences.id_company).id_user
            registrations = Register.objects.get(id=Experiences.id_user)
            if (registrations.token == 'xxx'):
                response = {'status':'LOGIN FIRST, YOU MUST...'}
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)
            else:    
                try:
                    token = request.META.get('HTTP_AUTHORIZATION','')
                    get_token = Register.objects.get(token = token)
                    if ((get_token.id == Experiences.id_user) | (get_token.id == company)):
                        if request.method == 'GET':
                            serializer = ExperiencesSerializer(Experiences)
                            act = 'Read experience by '                           
                            read_log(request, registrations,act)
                            return Response(serializer.data)
                        elif request.method == 'PUT':                
                            serializer = ExperiencesSerializer(Experiences, data=request.data)
                            if serializer.is_valid():
                                serializer.save()
                                act = 'Update experience by '
                                update_log(request, registrations, act)
                                return Response(serializer.data, status=status.HTTP_201_CREATED)
                            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                    else:
                        content = {
                        'status': 'UNAUTHORIZED'
                        }
                        return Response(content, status=status.HTTP_401_UNAUTHORIZED)
                    
                except Register.DoesNotExist:
                    content = {
                        'status': 'Not found in register'
                    }
                    return Response(content, status=status.HTTP_404_NOT_FOUND)
        except pengalaman.DoesNotExist:
            content = {
                'status': 'Not Found in Experience'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def get_post_experiences(request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION')
        is_authentication(token)

        if request.method == 'GET':
            network = pengalaman.objects.all()
            serializer = ExperiencesSerializer(network, many=True)

            response = {
                'api_status': status.HTTP_200_OK,
                'api_message': 'Update data experience berhasil',
                'data': serializer.data
            }

            return JsonResponse(response)

        elif request.method == 'POST':
            serializer = ExperiencesSerializer(data=request.query_params)
            if serializer.is_valid():
                serializer.save()

                response = {
                    'api_status': status.HTTP_200_OK,
                    'api_message': 'Update data berhasil',
                    'data': serializer.data
                }

                return JsonResponse(response)
    except Exception as ex:
        response = {
            'api_error': status.HTTP_400_BAD_REQUEST,
            'api_status': str(ex.args)
        }

        return JsonResponse(response)


@api_view(['GET'])
def get_post_experiences_user(request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION')
        is_authentication(token)

        if request.method == 'GET':
            network = pengalaman.objects.all().filter(id_user=int(request.query_params['id_user']))
            serializer = ExperiencesSerializer(network, many=True)

            response = {
                'api_status': status.HTTP_200_OK,
                'api_message': 'Update data berhasil',
                'data': serializer.data
            }

            return JsonResponse(response)

    except Exception as ex:
        response = {
            'api_error': status.HTTP_400_BAD_REQUEST,
            'api_status': str(ex.args)
        }

        return JsonResponse(response)





