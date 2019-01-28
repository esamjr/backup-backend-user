from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import json
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Business
from .serializers import BusinessSerializer, JoincompanySerializer, RegSerializer, JoincompanySerializer2
from registrations.models import Register
from join_company.models import Joincompany
from django.db.models import Q

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

@api_view(['POST'])
def custom_get_one(request, pk):
    if request.method == 'POST':
        # comp_name = request.data['business_id']
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            id_users = Register.objects.get(token = token)            
            get_id_comp = Business.objects.get(id = pk)

            get_id_join = Joincompany.objects.all().filter(status="1",id_company = pk)
            serializer1 = JoincompanySerializer(data =get_id_join, many = True)
            if serializer1.is_valid():
                serializer2 = BusinessSerializer(get_id_comp)
                serializer3 = {'status':serializer1.data,
                               'Company':serializer2.data}               
                return Response(serializer3, status=status.HTTP_201_CREATED)
            else:
                response = {'status':'did not have any..'}
                return Response(response, status=status.HTTP_404_NOT_FOUND)

        except Joincompany.DoesNotExist:
            response = {'status':'TRY TO APPLY JOB FIRST, YOU MUST ...'}
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        except Business.DoesNotExist:
            response = {'status':'MAKE BUSINESS ACCOUNT FIRST, YOU MUST ...'}
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)    
        except Register.DoesNotExist:
            response = {'status':'LOGIN FIRST, YOU MUST ...'}
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        # except:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def custom_get_two(request, pk):
    if request.method == 'POST':
        # comp_name = request.data['business_id']
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            id_users = Register.objects.get(token = token)            
            get_id_comp = Business.objects.get(id = pk)

            get_id_join = Joincompany.objects.all().filter(status="2",id_company = pk)
            serializer1 = JoincompanySerializer(data = get_id_join, many = True)
            if serializer1.is_valid():
                serializer2 = BusinessSerializer(get_id_comp)
                serializer3 = {'status':serializer1.data,
                               'Company':serializer2.data}
                return Response(serializer3, status=status.HTTP_201_CREATED)
            else:
                response = {'status':'did not have any..'}
                return Response(response, status=status.HTTP_404_NOT_FOUND)              
                
        except Joincompany.DoesNotExist:
            response = {'status':'TRY TO APPLY JOB FIRST, YOU MUST ...'}
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        except Business.DoesNotExist:
            response = {'status':'MAKE BUSINESS ACCOUNT FIRST, YOU MUST ...'}
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)    
        except Register.DoesNotExist:
            response = {'status':'LOGIN FIRST, YOU MUST ...'}
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        # except:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def search_company(request):
    if request.method == 'GET':        
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            tokens = Register.objects.get(token=token)
            users_id = tokens.id
            get_id_join = Joincompany.objects.all().values('id_company').filter(user_id = users_id).exclude(Q(status="1") | Q(status="2"))
            # get_id = 
            # serializer = JoincompanySerializer(get_id_join, many=True)
            # get_id_join = Joincompany.objects.all().values('id_company').filter(Q(status="1") | Q(status="2"), user_id = users_id)
            # for x in get_id_join:
            #     y = 0
            #     get_id = [x]
            #     y+=1
            # x=JoincompanySerializer(get_id_join)
            # gets = get_id_join['id_company']
            # for gets in get_id_join:
            #     gone = []
            #     gone.append(gets)

            # for x in get_id_join:
            #     get_comp = Business.objects.get(id=x)
            #     serializer = BusinessSerializer(get_comp)
            #     # return Response(serializer.data, status=status.HTTP_201_CREATED)
            #     ser = str(serilaizer.data)
            #     company = company.update(ser)
            #     return print(serializer)
            # get_comp = get_id_join
            # idnya = get_object_or_404(Business, id = get_id_join)
            # get_id_comp = Business.objects.filter(id__exact = get_id_join['id_company'])

            # # id_comp = get_id_comp.id
            # serializer1 = JoincompanySerializer(get_id_join, many = True)
            # serializer2 = BusinessSerializer(get_id_comp)
            # # if serializer1.is_valid():
            # serializer3 = {'status':[serializer1.data],
                           # 'Company':serializer2.data}
            # return Response(json.dumps(company))

            return Response(get_id_join, status=status.HTTP_201_CREATED)
        
            # response = {'status':'did not have any..'}
            # return Response(response, status=status.HTTP_404_NOT_FOUND)      
            
        except Joincompany.DoesNotExist:
            response = {'status':'TRY TO APPLY JOB FIRST, YOU MUST ...'}
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        except Business.DoesNotExist:
            response = {'status':'MAKE BUSINESS ACCOUNT FIRST, YOU MUST ...'}
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)    
        except Register.DoesNotExist:
            response = {'status':'LOGIN FIRST, YOU MUST ...'}
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        # except Exception:
        #     return Response({'ERRORS'}, status=status.HTTP_400_BAD_REQUEST)