from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .models import LicenseComp
from .serializers import LicenseCompSerializer
from registrations.models import Register
from hierarchy.models import Hierarchy
from business_account.models import Business

@api_view(['GET','PUT', 'POST'])
def setting_license_company(request,pk):
    if request.method == 'POST':        
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
            user = Register.objects.get(token = token)
            company = Business.objects.get(id = pk ,id_user = user.id)
            hierarchy_comp = Hierarchy.objects.all().values_list('division', flat=True).filter(id_company = company.id)
            result = []
            for inst in hierarchy_comp:
                payload = {
                            'id_hierarchy': inst,
                            'attendance':'0',
                            'payroll':'0',
                            'status':'0'
                        }
                serializer = LicenseCompSerializer(data = payload)
                if serializer.is_valid():
                    serializer.save()
                    result.append(serializer.data)
            return Response(result, status = status.HTTP_201_CREATED)
        except Register.DoesNotExist:
            return Response({'status':'User Does Not Exist'}, status = status.HTTP_400_BAD_REQUEST)
        except Business.DoesNotExist:
            return Response({'status':'Company Does Not Exist'}, status = status.HTTP_400_BAD_REQUEST)
        except Hierarchy.DoesNotExist:
            return Response({'status':'Hierarchy Does Not Exist'}, status = status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PUT':
        license_company = LicenseComp.objects.get(id = pk)
        serializer = LicenseCompSerializer(license_company, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        try:
            beacon = LicenseComp.objects.get(id = pk)
            serializer = LicenseCompSerializer(beacon)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        except LicenseComp.DoesNotExist:
            return Response({'status':'License Company Does Not Exist'}, status = status.HTTP_400_BAD_REQUEST)




# @api_view(['GET', 'DELETE', 'PUT'])
# def get_delete_update_historyhierarchy(request, pk):
#     try:
#         history_hierarchy = Historyhierarchy.objects.get(pk=pk)
#     except Historyhierarchy.DoesNotExist:
#         content = {
#             'status': 'Not Found'
#         }
#         return Response(content, status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == 'GET':
        
#         serializer = HistoryhierarchySerializer(history_hierarchy)
#         users = Register.objects.get(id = serializer.data['id_user'])

#         return Response({'nama':users.full_name,'data':serializer.data})

#     elif request.method == 'DELETE':
        
#             history_hierarchy.delete()
#             content = {
#                 'status' : 'NO CONTENT'
#             }
      
#     elif request.method == 'PUT':
        
#             serializer = HistoryhierarchySerializer(history_hierarchy, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      

# @api_view(['GET', 'POST'])
# def get_post_historyhierarchy(request):
#     if request.method == 'GET':
#         network = Historyhierarchy.objects.all()        
#         datas = []
#         for nets in network:
#             serializer = HistoryhierarchySerializer(nets)
#             users = Register.objects.get(id = serializer.data['id_user'])
#             sets = {'nama':users.full_name,'data':serializer.data}
#             datas.append(sets)
#         return Response(datas)

#     elif request.method == 'POST':
#         serializer = HistoryhierarchySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# def get_all_historyhierarchy(request, pk):
#     try:
#         network = Historyhierarchy.objects.all().filter(id_company=pk)
#         datas = []
#         for nets in network:
#             serializer = HistoryhierarchySerializer(nets)
#             users = Register.objects.get(id = serializer.data['id_user'])
#             sets = {'nama':users.full_name,'data':serializer.data}
#             datas.append(sets)
#         return Response(datas)
#     except Historyhierarchy.DoesNotExist:
#         content = {
#             'status': 'Not Found'
#         }
#         return Response(content, status=status.HTTP_404_NOT_FOUND)
