from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from registrations.models import Register
from .models import Joincompany
from .serializers import JoincompanySerializer


@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_joincompany(request, pk):
    try:
        token = request.META.get('HTTP_AUTHORIZATION')
        user = Register.objects.get(token=token)
    except Register.DoesNotExist:
        content = {
            'status': 'UNAUTHORIZED'
        }
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)

    join_company = Joincompany.objects.get(id=pk)
    if request.method == 'GET':
        serializer = JoincompanySerializer(join_company)
        return Response(serializer.data)
    elif request.method == 'DELETE':

        content = {
            'status': 'EXTERMINATE...EXTERMINATE...'
        }
        join_company.delete()
        return Response(content, status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = JoincompanySerializer(join_company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def get_post_joincompany(request):
    if request.method == 'GET':
        network = Joincompany.objects.all()
        serializer = JoincompanySerializer(network, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        id_user = int(request.data['id_user'])
        id_check = Joincompany.objects.filter(id_user=id_user).exists()
        if id_check:
            content = {
                'status': 'Email already exist'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        serializer = JoincompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_post_joincompany_user(request, pk):
    try:
        if request.method == 'GET':
            network = Joincompany.objects.all().filter(id_user=pk)
            serializer = JoincompanySerializer(network, many=True)
            return Response(serializer.data)

    except Joincompany.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def join_company_by_active(request, pk):
    token = request.META.get('HTTP_AUTHORIZATION')
    try:
        user = Register.objects.get(token=token).id
        beacon = Joincompany.objects.get(id_company=pk, status="2", id_user=user)
        serializer = JoincompanySerializer(beacon)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Register.DoesNotExist:
        response = {'status': 'USER DOES NOT EXIST'}
        return Response(response, status=status.HTTP_404_NOT_FOUND)
    except Joincompany.DoesNotExist:
        response = {'status': 'JOIN COMPANY DOES NOT EXIST'}
        return Response(response, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def server_integration(request):
    if request.method == 'GET':
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
            user = Register.objects.get(token=token)
            comp = Joincompany.objects.get(id_user=user.id,
                                           status="2")  # tidak bisa mengambil jika user bergabung dengan berbagai perusahaan
            return Response(comp.id_company, status=status.HTTP_202_ACCEPTED)
        except Register.DoesNotExist:
            return Response({'status': 'UNAUTHORIZED'}, status=status.HTTP_401_UNAUTHORIZED)
