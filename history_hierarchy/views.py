from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from business_account.helper import cek_company_id
from registrations.models import Register
from .models import Historyhierarchy
from .serializers import HistoryhierarchySerializer


@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_historyhierarchy(request, pk):
    try:
        history_hierarchy = Historyhierarchy.objects.get(pk=pk)
    except Historyhierarchy.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':

        serializer = HistoryhierarchySerializer(history_hierarchy)
        users = Register.objects.get(id=serializer.data['id_user'])

        return Response({'nama': users.full_name, 'data': serializer.data})

    elif request.method == 'DELETE':

        history_hierarchy.delete()
        content = {
            'status': 'NO CONTENT'
        }

    elif request.method == 'PUT':

        serializer = HistoryhierarchySerializer(history_hierarchy, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def get_post_historyhierarchy(request):
    if request.method == 'GET':
        network = Historyhierarchy.objects.all()
        datas = []
        for nets in network:
            serializer = HistoryhierarchySerializer(nets)
            users = Register.objects.get(id=serializer.data['id_user'])
            sets = {'nama': users.full_name, 'data': serializer.data}
            datas.append(sets)
        return Response(datas)

    elif request.method == 'POST':
        serializer = HistoryhierarchySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_all_historyhierarchy(request):
    try:
        id_company = request.query_params['id_company']
        _is_company = cek_company_id(id_company)
        if not _is_company:
            response = {
                'api_status': status.HTTP_404_NOT_FOUND,
                'api_message': 'Company tidak ada',
            }

            return JsonResponse(response)

        network = Historyhierarchy.objects.all().filter(id_company=_is_company)
        datas = []
        for nets in network:
            serializer = HistoryhierarchySerializer(nets)
            users = Register.objects.get(id=serializer.data['id_user'])
            sets = {'nama': users.full_name, 'data': serializer.data}
            datas.append(sets)
        return Response(datas)

    except Exception as ex:
        response = {
            'api_error': str(ex),
            'api_message': ex.args
        }

        return JsonResponse(response)
