from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .models import LicenseComp
from .serializers import LicenseCompSerializer
from registrations.models import Register
from hierarchy.models import Hierarchy
from business_account.models import Business

@api_view(['GET'])
def search_all_div(request):
    try:
        beacon = LicenseComp.objects.all().values_list('id', flat = True)
        result = []
        for one in beacon:
            beaco = LicenseComp.objects.get(id = one)
            serializer = LicenseCompSerializer(beaco)
            dive = Hierarchy.objects.get(id = serializer.data['id_hierarchy'])
            payload = {
            'division': dive.division ,
            'data' : serializer.data
            }
            result.append(payload)            
        return Response(result, status = status.HTTP_201_CREATED)
    except LicenseComp.DoesNotExist:
        return Response({'status':'License Company Does Not Exist'}, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT', 'POST'])
def setting_license_company(request,pk):
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
                            'attendance':'0',
                            'payroll':'0',
                            'status':'0',
                            'id_comp':company.id
                        }
                serializer = LicenseCompSerializer(data = payload)
                if serializer.is_valid():
                    serializer.save()
                    result.append(serializer.data)
            return Response(result, status = status.HTTP_201_CREATED)
            # -----------------START TESTING CODE---------------
            # hierarchy_comp = Hierarchy.objects.get(id_company = company.id, division = 'CTO').id
            # payload = {
            #             'id_hierarchy': hierarchy_comp,
            #             'attendance':'0',
            #             'payroll':'0',
            #             'status':'0',
            #             'id_comp':company.id
            #         }          
            # serializer = LicenseCompSerializer(data = payload)
            # if serializer.is_valid():
            #     serializer.save()
            #     return Response(serializer.data, status = status.HTTP_201_CREATED)
            # return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            #-----------------END TESTING CODE------------------
        elif request.method == 'PUT':
            license_company = LicenseComp.objects.get(id = pk)
            serializer = LicenseCompSerializer(license_company, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'GET':
            try:
                # beacon = LicenseComp.objects.get(id = pk)
                # serializer = LicenseCompSerializer(beacon)
                beacon = LicenseComp.objects.all().values_list('id', flat = True).filter(id_comp = pk)
                result = []
                for one in beacon:
                    beaco = LicenseComp.objects.get(id = one)
                    serializer = LicenseCompSerializer(beaco)
                    dive = Hierarchy.objects.get(id = serializer.data['id_hierarchy'])
                    payload = {
                    'division': dive.division ,
                    'data' : serializer.data
                    }
                    result.append(payload)            
                return Response(result, status = status.HTTP_201_CREATED)
            except LicenseComp.DoesNotExist:
                return Response({'status':'License Company Does Not Exist'}, status = status.HTTP_400_BAD_REQUEST)
            
    except Register.DoesNotExist:
        return Response({'status':'User Does Not Exist'}, status = status.HTTP_404_NOT_FOUND)
    except Business.DoesNotExist:
        return Response({'status':'Company Does Not Exist'}, status = status.HTTP_404_NOT_FOUND)
    except Hierarchy.DoesNotExist:
        return Response({'status':'Hierarchy Does Not Exist'}, status = status.HTTP_400_BAD_REQUEST)
    except LicenseComp.DoesNotExist:
        return Response({'status':'License Company Does Not Exist'}, status = status.HTTP_400_BAD_REQUEST)
    
    