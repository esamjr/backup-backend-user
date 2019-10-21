from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .models import Groups
from .serializers import GroupsSerializer
from registrations.models import Register
from hierarchy.models import Hierarchy
from business_account.models import Business

@api_view(['GET'])
def search_all_div(request):
    try:
        beacon = Groups.objects.all().values_list('id', flat = True)
        result = []
        for one in beacon:
            beaco = Groups.objects.get(id = one)
            serializer = GroupsSerializer(beaco)
            dive = Hierarchy.objects.get(id = serializer.data['id_hierarchy'])
            user = Register.objects.get(id = dive.id_user)
            persona = {
            'id_user' : user.id,
            'name' : user.full_name
            }
            payload = {
            'division': dive.division ,
            'data' : serializer.data,
            'user' : persona
            }
            result.append(payload)            
        return Response(result, status = status.HTTP_201_CREATED)
    except Groups.DoesNotExist:
        return Response({'status':'Groups Does Not Exist'}, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT', 'POST'])
def setting_groups(request,pk):
    try:
        if request.method == 'POST': 
        
            token = request.META.get('HTTP_AUTHORIZATION')
            user = Register.objects.get(token = token)
            company = Business.objects.get(id = pk ,id_user = user.id)
            
            hierarchy_comp = Hierarchy.objects.all().values_list('id', flat=True).filter(id_company = company.id)
            result = []
            for inst in hierarchy_comp:                
                payload = {
                            'id_hierarchy': inst,
                            'tipe_group':'0',
                            'parent_group':'0',
                            'set_manage':'0',                            
                            'set_view':'0',
                            'id_company':company.id
                        }
                serializer = GroupsSerializer(data = payload)
                if serializer.is_valid():
                    serializer.save()
                    result.append(serializer.data)
            return Response(result, status = status.HTTP_201_CREATED)
            
        elif request.method == 'PUT':
            license_company = Groups.objects.get(id = pk)
            serializer = GroupsSerializer(license_company, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'GET':
            try:
               
                beacon = Groups.objects.all().values_list('id', flat = True).filter(id_company = pk)
                result = []
                for one in beacon:
                    beaco = Groups.objects.get(id = one)
                    serializer = GroupsSerializer(beaco)
                    dive = Hierarchy.objects.get(id = serializer.data['id_hierarchy'])
                    user = Register.objects.get(id = dive.id_user)
                   
                    persona = {
                    'id_user' : user.id,
                    'name' : user.full_name
                    }
                    if(serializer.data['parent_group']>0):
                        divee = Hierarchy.objects.get(id = serializer.data['parent_group'])
                       
                        parent={
                            'id_user' : divee.id,
                            'name' : divee.division
                        }
                    else:
                        parent={
                            'id_user' : 0,
                            'name' : ''
                        }
                    payload = {
                    'division': dive.division ,
                    'data' : serializer.data,
                    'user':persona,
                    'parent': parent
                    }
                    result.append(payload)            
                return Response(result, status = status.HTTP_201_CREATED)
            except Groups.DoesNotExist:
                return Response({'status':'License Company Does Not Exist'}, status = status.HTTP_400_BAD_REQUEST)
            
    except Register.DoesNotExist:
        return Response({'status':'User Does Not Exist'}, status = status.HTTP_404_NOT_FOUND)
    except Business.DoesNotExist:
        return Response({'status':'Company Does Not Exist'}, status = status.HTTP_404_NOT_FOUND)
    except Hierarchy.DoesNotExist:
        return Response({'status':'Hierarchy Does Not Exist'}, status = status.HTTP_400_BAD_REQUEST)
    except Groups.DoesNotExist:
        return Response({'status':'Groups Does Not Exist'}, status = status.HTTP_400_BAD_REQUEST)
    
    