from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from log_app.views import create_log, read_log, update_log, delete_log
from registrations.models import Register
from .models import Award as award
from .serializers import AwardSerializer


@api_view(['GET','DELETE', 'PUT'])
def get_delete_update_award(request, pk):
   
    try:
        Award = award.objects.get(pk=pk)
        registrations = Register.objects.get(pk=Award.id_user)
        if (registrations.token == 'xxx'):
            response = {'status':'LOGIN FIRST, YOU MUST...'}
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        else:    
            try:
                token = request.META.get('HTTP_AUTHORIZATION','')
                get_token = Register.objects.get(token = token) 
                if (get_token.id == Award.id_user):
                    if request.method == 'GET':
                        serializer = AwardSerializer(Award)
                        act = 'Read Award by '                           
                        read_log(request, registrations, act)
                        return Response(serializer.data)

                    elif request.method == 'DELETE':
                        if (Award.verified == "0"):
                            act = 'Delete award by id : '                           
                            delete_log(request, registrations, Award.award, act)                                         
                            Award.delete()
                            content = {
                                'status' : 'NO CONTENT'
                            }
                            return Response(content, status=status.HTTP_204_NO_CONTENT)
                        else:
                            content={'status':'Cannot touch this, because your award already verified'}
                            return Response(content, status=status.HTTP_401_UNAUTHORIZED)                         
                    elif request.method == 'PUT':

                            serializer = AwardSerializer(Award, data=request.data)
                            if serializer.is_valid():
                                act = 'Update certification by '
                                update_log(request, registrations, act)
                                serializer.save()
                                return Response(serializer.data, status=status.HTTP_201_CREATED)
                            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    content = {
                    'status': 'UNAUTHORIZED'
                    }
                    return Response(content, status=status.HTTP_401_UNAUTHORIZED)
                    
            except Register.DoesNotExist:
                content = {
                    'status': 'UNAUTHORIZED'
                }
                return Response(content, status=status.HTTP_401_UNAUTHORIZED)

    except Register.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def get_post_award(request):
    try:
        if request.method == 'GET':
            network = award.objects.all()
            serializer = AwardSerializer(network, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = AwardSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except award.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_post_award_user(request,pk):
    token = request.META.get('HTTP_AUTHORIZATION')
    registrations = Register.objects.get(token =token)

    try:
        if request.method == 'GET':
            network = award.objects.all().filter(id_user=pk)
            serializer = AwardSerializer(network, many=True)
            act = 'Read all award by '                           
            read_log(request, registrations,act)
            return Response(serializer.data)
    except award.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)
