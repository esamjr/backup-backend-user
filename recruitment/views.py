from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Jobs, Recruitment
from .serializers import JobSerializer, RecSerializer, StatusApplySerializer
from registrations.models import Register
from registrations.serializers import RegisterSerializer
from join_company.models import Joincompany
from join_company.serializers import JoincompanySerializer
from business_account.models import Business
from log_app.views import create_log, read_log, update_log, delete_log
from log_app.serializers import LoggingSerializer
from log_app.models import Logging
from email_app.views import intervied_email
import time

@api_view(['GET', 'POST'])
def get_post_jobs(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    user = Register.objects.get(token = token)
    
    if request.method == 'POST':
        # join = Joincompany.objects.get(id_user = user.id, status="2").id_company
        payload = {
            'position' : request.data['position'],
            'comp_id' : request.data['comp_id'],
            'descript' : request.data['descript'],
            'sallary' : request.data['sallary'],
            'location' : request.data['location'],
            'deadline' : request.data['deadline'],
            'pref_language' : request.data['pref_language'],
            'dresscode' : request.data['dresscode'],
            'worktime' : request.data['worktime'],
            'tunjangan' : request.data['tunjangan']
        }
        serializer = JobSerializer(data = payload)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    elif request.method =='GET':
        network = Jobs.objects.all().values_list('id', flat = True)
        datas = []
        for net in network:
            beac = Jobs.objects.get(id = net)
            serializer = JobSerializer(beac)
            beaco = Business.objects.get(id = serializer.data['comp_id'])
            sets = {'comp_name': beaco.company_name, 'logo':beaco.logo_path ,'data':serializer.data}
            datas.append(sets)

        return Response(datas , status = status.HTTP_201_CREATED)

@api_view(['GET','DELETE', 'PUT'])
def get_delete_put_jobs(request, pk):
    beacon = Jobs.objects.get(id = pk)
    if request.method == 'GET':        
        serializer = JobSerializer(beacon)
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        beacon.delete()        
        return Response({'status':'Success Delete'}, status = status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = JobSerializer(beacon, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors ,status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST','PUT'])
def apply(request,pk):
    if request.method == 'POST':
        get_token = request.META.get('HTTP_AUTHORIZATION')
        id_user = Register.objects.get(token = get_token).id
        desc = request.data['desc']
        payload = {
            'id_jobs': pk,
            'id_applicant' : id_user,  
            'status': 0,
            'descript':desc
        }
        serializer = RecSerializer(data = payload)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        try:
            get_token = request.META.get('HTTP_AUTHORIZATION')
            rec = Recruitment.objects.get(id = pk)
            jobs = Jobs.objects.get(id = rec.id_jobs).comp_id
            busines = Business.objects.get(id = jobs)
            admin = Register.objects.get(id = busines.id_user)

            if admin.token == get_token:
                payload = {                
                'status':request.data['status']
                }                
                serializer = StatusApplySerializer(rec, data = request.data)
                if serializer.is_valid():
                    serializer.save()
                    if serializer.data['status'] == 1:
                        mail = Register.objects.get(id = id_applicant).email
                        date = request.data['tanggal']
                        time = request.data['waktu']
                        place = request.data['tempat']
                        compname = busines.company_name
                        intervied_email(request, compname, mail, date, time, place)
                    return Response(serializer.data, status = status.HTTP_200_OK)
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            return Response({'status':'Unauthorized'}, status = status.HTTP_401_UNAUTHORIZED)
        except Recruitment.DoesNotExist:
            return Response({'status':'Recruitment Does Not Exist'}, status = status.HTTP_404_NOT_FOUND)
        except Jobs.DoesNotExist:
            return Response({'status':'Jobs Does Not Exist'}, status = status.HTTP_404_NOT_FOUND)
        except Business.DoesNotExist:
            return Response({'status':'Business Does Not Exist'}, status = status.HTTP_404_NOT_FOUND)
        except Register.DoesNotExist:
            return Response({'status':'User Does Not Exist'}, status = status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def search_by_id_rec(request,pk):
    try:
        obj = Recruitment.objects.get(id = pk)
        serializer = RecSerializer(obj)        
        return Response(serializer.data ,status = status.HTTP_201_CREATED)
    except Recruitment.DoesNotExist:
        return Response({'status':'No Jobs With that ID'}, status = status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def find_applicant(request, pk):
    try:
        beacon = Recruitment.objects.all().filter(id_jobs = pk, status = 0)
        datas = []
        for var in beacon:
            serializer = RecSerializer(var)
            nets = Register.objects.get(id = serializer.data['id_applicant'])
            serialReg = RegisterSerializer(nets)
            netwo = {'data_applicant':serialReg.data, 'data_jobs':serializer.data}
            datas.append(netwo)
        return Response(datas, status = status.HTTP_201_CREATED)
    except Recruitment.DoesNotExist:
        return Response({'status':'Does Not Exist'}, status = status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def search(request,pk):   
    if pk == '1': #by status recruitment = 1 (reviewing)
        try:
            obj = Recruitment.objects.all().filter(status = 1)
            serializer = RecSerializer(obj, many = True)            
            return Response(serializer.data ,status = status.HTTP_201_CREATED)            
        except Recruitment.DoesNotExist:
            return Response({'status':'Does Not Exist'}, status = status.HTTP_204_NO_CONTENT)
        # except Exception:
        #     return Response({'status':'Does Not Exist'}, status = status.HTTP_400_BAD_REQUEST)

    elif pk == '2': #by status recruitment = 2 (interviewed)
        obj = Recruitment.objects.all().filter(status = 2)
        serializer = RecSerializer(obj, many = True)
        try:
            return Response(serializer.data ,status = status.HTTP_201_CREATED)
        except Exception:
            return Response({'status':'ERROR'}, status = status.HTTP_400_BAD_REQUEST)
    elif pk == '3': #by id users
        obj = Recruitment.objects.all().filter(id_applicant = pk)
        serializer = RecSerializer(obj, many = True)
        user = Register.objects.get(id = pk)
        regser = RegisterSerializer(user)
        try:
            return Response({'Bio':regser.data,'Data':serializer.data} ,status = status.HTTP_201_CREATED)
        except Exception:
            return Response({'status':'ERROR'}, status = status.HTTP_400_BAD_REQUEST)
    elif pk == '4': #by own id
        token = request.META.get('HTTP_AUTHORIZATION')
        user = Register.objects.get(token = token).id
        obj = Recruitment.objects.all().filter(id_applicant = user)
        serializer = RecSerializer(obj, many = True)        
        try:
            return Response(serializer.data ,status = status.HTTP_201_CREATED)
        except Exception:
            return Response({'status':'ERROR'}, status = status.HTTP_400_BAD_REQUEST)
        
    elif pk == '5': #transfer data from recruitment to join company 
        obj = Recruitment.objects.all().values_list('id','id_jobs', 'id_user').filter(status = 2)
        for id_rec, jobs, user in obj:
            comp = Jobs.objects.get(id = jobs).comp_id
            payload = {
                'id_user' : user,
                'id_company' : comp,
                'status' : "2",
                'id_rec' : id_rec
            }
            serializer = JoincompanySerializer(data = payload)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status =status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)