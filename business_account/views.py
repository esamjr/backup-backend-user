from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Business
from .serializers import BusinessSerializer, SearchSerializer, CustomJoincompanySerializer, JoincompanySerializer, RegSerializer
from registrations.models import Register
from join_company.models import Joincompany

@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_businessaccount(request, pk):
    try:
        Businessaccount = Business.objects.get(pk=pk)
        token = request.META.get('HTTP_AUTHORIZATION')
        user = Register.objects.get(token=token)
        if (token == 'xxx'):
            content = {
            'status': 'YOU SHALL NOT PASS'
            }
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)
        else:
            if (user.id==Businessaccount.id_user):
                if request.method == 'GET':
                    serializer = BusinessSerializer(Businessaccount)
                    return Response(serializer.data)

                elif request.method == 'DELETE':                    
                        Businessaccount.delete()
                        content = {
                            'status' : 'NO CONTENT'
                        }
                        return Response(content, status=status.HTTP_202_NO_CONTENT)
                   
                elif request.method == 'PUT':                    
                        serializer = BusinessSerializer(Businessaccount, data=request.data)
                        if serializer.is_valid():
                            serializer.save()
                            return Response(serializer.data, status=status.HTTP_201_CREATED)
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)                    
            else:
                content = {
                'status': 'UNAUTHORIZED'
                }
                return Response(content, status=status.HTTP_401_UNAUTHORIZED)

    except Business.DoesNotExist:
        content = {
            'status': 'Business does not exist'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)

    except Register.DoesNotExist:
        content = {
            'status': 'Token does not valid'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST'])
def get_post_businessaccount(request):
    if request.method == 'GET':
        network = Business.objects.all()
        serializer = BusinessSerializer(network, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BusinessSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_businessaccount(request, pk):
    try:
        network = Business.objects.all().filter(id_user = pk)
        serializer = BusinessSerializer(network, many=True)
        return Response(serializer.data)
    except Business.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def custom_get_all_businessaccount(request, pk):
    try:
        network = Joincompany.objects.all().filter(id_company = pk, status="1").id_user
        # serializer = CustomJoincompanySerializer(network, many=True)
        user = Register.objects.get().filter(id = network)
        serializer2 = RegSerializer(user, many=True)
        # if (serializer.data == []):
        #     return Response({'status zero'})
        return Response(serializer.data)
    except Business.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def search_company(request):
    if request.method == 'GET':
        # token = request.META.get('HTTP_AUTHORIZATION')
        # id_user = Register.objects.get(token = token).id
        comp_name = request.data['name_comp']
        state = Joincompany.objects.get(status="3"or"4")
        # search = Business.objects.filter(company_name__icontains = comp_name).all()
        user = Register.objects.get(id = str(state.id_user))
        # join_comp = Joincompany.objects.all().filter(search)
        # search = Joincompany.objects.all()
        serializer = RegSerializer(user, many = True)

        # if (join_comp.status == "1"):
        #     pass
        # else:
        return Response(user, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 0 = belum apa apa
# 1 = apply
# 2 = accepted
# 3 = denied 
# 4 = resign