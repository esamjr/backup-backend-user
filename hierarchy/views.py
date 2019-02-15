from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Hierarchy as Hierarchy_models
from level.models import Level
from registrations.models import Register
from .serializers import HierarchySerializer, UserSerializer

@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_hierarchy(request, pk):
    token = request.META.get('HTTP_AUTHORIZATION')
    try:
        user = Register.objects.get(token = token)
    except Register.DoesNotExist:        
        content = {
            'status': 'UNAUTHORIZED'
        }
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)
    try:
        Hierarchy = Hierarchy_models.objects.get(pk=pk)
        if request.method == 'GET':
            serializer = HierarchySerializer(Hierarchy)
            return Response(serializer.data)
        elif request.method == 'DELETE':           
                Hierarchy.delete()
                content = {
                    'status' : 'NO CONTENT'
                }
                return Response(content, status=status.HTTP_202_NO_CONTENT)
        elif request.method == 'PUT':            
                serializer = HierarchySerializer(Hierarchy, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)           

    except Hierarchy_models.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def get_post_hierarchy(request):
    if request.method == 'GET':
        network = Hierarchy_models.objects.all()
        serializer = HierarchySerializer(network, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = HierarchySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_hierarchy_by_user(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    company = request.data['id_company']
    user = Register.objects.get(token = token).id
    try:
        beacon = Hierarchy.objects.get(id_user = user, id_company = company)
        serializer = HierarchySerializer(beacon)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Hierarchy.DoesNotExist:
        response = {'status':'HIERARCHY DOES NOT EXIST'}
        return Response(response, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_all_hierarchy(request, pk1):
    # token = request.META.get('HTTP_AUTHORIZATION')
    # try:
    #     user = Register.objects.get(token = token)
    # except Register.DoesNotExist:        
    #     content = {
    #         'status': 'UNAUTHORIZED'
    #     }
    #     return Response(content, status=status.HTTP_401_UNAUTHORIZED)

    try:        
        results = []        
        networks = Hierarchy_models.objects.all().values_list('id', flat=True).filter(id_company=pk1)
        for network in networks:            
            hirarki = Hierarchy_models.objects.get(id=network)
            id_user = hirarki.id_user
            if id_user == 0:
                serializer = HierarchySerializer(hirarki)                
                dbase = {'hirarki':serializer.data, 'user':None }
                results.append(dbase)
            else :   
                user = Register.objects.get(id = id_user)
                serializer = HierarchySerializer(hirarki)
                serializer2 = UserSerializer(user)
                dbase = {'hirarki':serializer.data, 'user':serializer2.data }
                results.append(dbase)
        return Response(results)
    except Hierarchy_models.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)
  