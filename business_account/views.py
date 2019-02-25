from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import json
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Business
from .serializers import BusinessSerializer, JoincompanySerializer, RegSerializer, JobconSerializer
from registrations.models import Register
from join_company.models import Joincompany
from job_contract.models import Jobcontract
from employee_sign.models import Employeesign
from employee_sign.serializers import EmployeesignSerializer
from hierarchy.serializers import HierarchySerializer
from hierarchy.models import Hierarchy
from django.db.models import Q

@api_view(['GET'])
def get_name(request,pk):
    if request.method == 'GET':
        try:
            network = Business.objects.get(id = pk) 
            return Response(network.company_name, status = status.HTTP_201_CREATED)
        except Business.DoesNotExist:
            return Response(None, status = status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def child_company_vendor(request, pk):
    if request.method == 'GET':
        try:
            beacon = Business.objects.all().filter(parent_company = pk)
            serializers = BusinessSerializer(beacon, many = True)
            return Response(serializers.data, status = status.HTTP_201_CREATED)
        except Business.DoesNotExist:
            response = {'status':'CHILD COMPANY DOES NOT EXIST'}
            return Response(response, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def buat_vendor(request,pk):
    if request.method == 'GET':
        Businessaccount = Business.objects.get(pk=pk)
        serializer = BusinessSerializer(Businessaccount)
        user = Register.objects.get(id = serializer.data['id_user'])
        userSerial = RegSerializer(user)
        try: 
            pba = Business.objects.get(id= serializer.data['parent_company'])
            pbaserial = BusinessSerializer(pba)
            pbanya = pbaserial.data
        except Business.DoesNotExist:
            pbanya = 'null'        
        result = [{'Business': serializer.data}, {'PBA':pbanya}, {'sA':userSerial.data}]
        return Response(result)

@api_view(['GET'])
def cakarsebek_vendor(request, pk):
    if request.method == 'GET':
        result =[]
        get_comp = Joincompany.objects.all().values_list('id_user', flat=True).filter(status = "2",id_company = pk)
        for user in get_comp:
            try:
                beacon =  Register.objects.get(id = user)
                karyawan = beacon.id
                perus = Joincompany.objects.get( status = "2", id_user = karyawan, id_company = pk)
                empsign = Employeesign.objects.get(id_user = perus.id_user, id_company = perus.id_company)
                hierarchy = Hierarchy.objects.get(id= empsign.id_hirarchy)
                job_contract = Jobcontract.objects.get(id = empsign.id_job_contract)
                serializerUser = RegSerializer(beacon)
                serilaizerComp = JoincompanySerializer(perus)
                serializerEmps = EmployeesignSerializer(empsign)
                serializerHier = HierarchySerializer(hierarchy)
                serializerJobcon = JobconSerializer(job_contract)
                people = {'user':serializerUser.data, 'join_company':serilaizerComp.data, 'job_contract' : serializerJobcon.data, 'employee_sign':serializerEmps.data, 'hierarchy':serializerHier.data}
                # people = {'user':serializerUser.data}
                result.append(people)        
                # return Response(result)
            except Employeesign.DoesNotExist:
                pass
                beacon =  Register.objects.get(id = user)
                karyawan = beacon.id
                perus = Joincompany.objects.get( status = "2", id_user = karyawan, id_company = pk)
                serializerUser = RegSerializer(beacon)
                serilaizerComp = JoincompanySerializer(perus)
                people = {'user':serializerUser.data, 'join_company':serilaizerComp.data, 'job_contract' : [], 'employee_sign':[], 'hierarchy':[]}
                result.append(people)
            except Jobcontract.DoesNotExist:
                pass
                beacon =  Register.objects.get(id = user)
                karyawan = beacon.id
                perus = Joincompany.objects.get( status = "2", id_user = karyawan, id_company = pk)
                empsign = Employeesign.objects.get(id_user = perus.id_user, id_company = perus.id_company)
                serializerEmps = EmployeesignSerializer(empsign)
                serializerUser = RegSerializer(beacon)
                serilaizerComp = JoincompanySerializer(perus)
                people = {'user':serializerUser.data, 'join_company':serilaizerComp.data, 'job_contract' : [], 'employee_sign':serializerEmps.data, 'hierarchy':[]}
                result.append(people)
            except Hierarchy.DoesNotExist:
                pass
                beacon =  Register.objects.get(id = user)
                karyawan = beacon.id
                perus = Joincompany.objects.get( status = "2", id_user = karyawan, id_company = pk)
                empsign = Employeesign.objects.get(id_user = perus.id_user, id_company = perus.id_company)
                job_contract = Jobcontract.objects.get(id = empsign.id_job_contract)
                serializerJobcon = JobconSerializer(job_contract)
                serializerEmps = EmployeesignSerializer(empsign)
                serializerUser = RegSerializer(beacon)
                serilaizerComp = JoincompanySerializer(perus)
                people = {'user':serializerUser.data, 'join_company':serilaizerComp.data, 'job_contract' : serializerJobcon.data, 'employee_sign':serializerEmps.data, 'hierarchy':[]}
                result.append(people)
        return Response(result) 

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
                    user = Register.objects.get(id = serializer.data['id_user'])
                    userSerial = RegSerializer(user)
                    try: 
                        pba = Business.objects.get(id= serializer.data['parent_company'])
                        pbaserial = BusinessSerializer(pba)
                        pbanya = pbaserial.data
                    except Business.DoesNotExist:
                        pbanya = 'null'
                    result = [{'Business': serializer.data}, {'PBA':pbanya}, {'sA':userSerial.data}]
                    return Response(result)

                elif request.method == 'DELETE':                    
                        Businessaccount.delete()
                        content = {
                            'status' : 'NO CONTENT'
                        }
                        return Response(content, status=status.HTTP_204_NO_CONTENT)
                   
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
        beacon = Business.objects.all().values_list('id', 'id_user', 'parent_company')
        result = []
        for comp, user, parent in beacon:
            ba = Business.objects.get(id= comp)
            baserial = BusinessSerializer(ba)
            try:
                network = Register.objects.get(id = user)
                serializer = RegSerializer(network)
                pba = Business.objects.get(id = parent)
                pbaserial = BusinessSerializer(pba)
                hasil = {'Business': baserial.data, 'PBA':pbaserial.data, 'SA':serializer.data}
                result.append(hasil)
            except Business.DoesNotExist:
                network = Register.objects.get(id = user)
                serializer = RegSerializer(network)
                pbanya = 'null'
                hasil = {'Business': baserial.data, 'PBA':pbanya, 'SA':serializer.data}
                result.append(hasil)           
        return Response(result)

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
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            user = Register.objects.get(token=token).id            
            result = []
            joins = Joincompany.objects.all().values_list('id_user', flat=True).filter(status="1", id_company=pk)
            for joi in joins:
                joincomp = Joincompany.objects.get(status="1", id_company=pk, id_user=joi)
                get_user = Register.objects.get(id = joi)
                dicx = RegSerializer(get_user)
                dic = {'user': dicx.data,'id_join_company':joincomp.id}                
                result.append(dic)               
            return Response(result)

        except Register.DoesNotExist:
            response = {'status':'LOGIN FIRST, YOU MUST ...'}
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)       
        except Joincompany.DoesNotExist:
            response = {'status':'TRY TO APPLY JOB FIRST, YOU MUST ...'}
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)       
        except:
            return Response({'ERRORS'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def custom_get_two(request, pk):
   if request.method == 'POST':        
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            user = Register.objects.get(token=token).id            
            result = []
            joins = Joincompany.objects.all().values_list('id_user', flat=True).filter(status="2", id_company=pk)
            for joi in joins:
                joincomp = Joincompany.objects.get(status="2", id_company=pk, id_user=joi)
                get_user = Register.objects.get(id = joi)
                dic = {'id': get_user.id,'fullname' : get_user.full_name, 'Birthday': get_user.birth_day,'id_join_company':joincomp.id}                
                result.append(dic)               
            return Response(result)

        except Register.DoesNotExist:
            response = {'status':'LOGIN FIRST, YOU MUST ...'}
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)       
        except Joincompany.DoesNotExist:
            response = {'status':'TRY TO APPLY JOB FIRST, YOU MUST ...'}
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)       
        except:
            return Response({'ERRORS'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def cakarsebek(request, pk):
    if request.method == 'GET':
        result =[]
        get_comp = Joincompany.objects.all().values_list('id_user', flat=True).filter(status = "2",id_company = pk)
        for user in get_comp:
            try:
                beacon =  Register.objects.get(id = user)
                karyawan = beacon.id
                perus = Joincompany.objects.get( status = "2", id_user = karyawan, id_company = pk)
                empsign = Employeesign.objects.get(id_user = perus.id_user, id_company = perus.id_company)
                hierarchy = Hierarchy.objects.get(id= empsign.id_hirarchy)
                job_contract = Jobcontract.objects.get(id = empsign.id_job_contract)
                serializerUser = RegSerializer(beacon)
                serilaizerComp = JoincompanySerializer(perus)
                serializerEmps = EmployeesignSerializer(empsign)
                serializerHier = HierarchySerializer(hierarchy)
                serializerJobcon = JobconSerializer(job_contract)
                people = {'user':serializerUser.data, 'join_company':serilaizerComp.data, 'job_contract' : serializerJobcon.data, 'employee_sign':serializerEmps.data, 'hierarchy':serializerHier.data}
                # people = {'user':serializerUser.data}
                result.append(people)        
                # return Response(result)
            except Employeesign.DoesNotExist:
                pass
                beacon =  Register.objects.get(id = user)
                karyawan = beacon.id
                perus = Joincompany.objects.get( status = "2", id_user = karyawan, id_company = pk)
                serializerUser = RegSerializer(beacon)
                serilaizerComp = JoincompanySerializer(perus)
                people = {'user':serializerUser.data, 'join_company':serilaizerComp.data, 'job_contract' : [], 'employee_sign':[], 'hierarchy':[]}
                result.append(people)
            except Jobcontract.DoesNotExist:
                pass
                beacon =  Register.objects.get(id = user)
                karyawan = beacon.id
                perus = Joincompany.objects.get( status = "2", id_user = karyawan, id_company = pk)
                empsign = Employeesign.objects.get(id_user = perus.id_user, id_company = perus.id_company)
                serializerEmps = EmployeesignSerializer(empsign)
                serializerUser = RegSerializer(beacon)
                serilaizerComp = JoincompanySerializer(perus)
                people = {'user':serializerUser.data, 'join_company':serilaizerComp.data, 'job_contract' : [], 'employee_sign':serializerEmps.data, 'hierarchy':[]}
                result.append(people)
            except Hierarchy.DoesNotExist:
                pass
                beacon =  Register.objects.get(id = user)
                karyawan = beacon.id
                perus = Joincompany.objects.get( status = "2", id_user = karyawan, id_company = pk)
                empsign = Employeesign.objects.get(id_user = perus.id_user, id_company = perus.id_company)
                job_contract = Jobcontract.objects.get(id = empsign.id_job_contract)
                serializerJobcon = JobconSerializer(job_contract)
                serializerEmps = EmployeesignSerializer(empsign)
                serializerUser = RegSerializer(beacon)
                serilaizerComp = JoincompanySerializer(perus)
                people = {'user':serializerUser.data, 'join_company':serilaizerComp.data, 'job_contract' : serializerJobcon.data, 'employee_sign':serializerEmps.data, 'hierarchy':[]}
                result.append(people)
        return Response(result)          

@api_view(['GET'])
def search_company(request):
    if request.method == 'GET':        
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            get_users = Register.objects.get(token=token).id
            result = []
            get_ba = Business.objects.all().values_list('id', flat=True)
            y = 0
            
            for ba in get_ba:
                bas = get_join(get_users,ba)
                bax = get_company(ba)
                coba = {'id_company':ba,'company':bax, 'join':bas}
                result.append(coba)
                y=y+1 
            return Response(result)
        except Register.DoesNotExist:
            response = {'status':'LOGIN FIRST, YOU MUST ...'}
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        
def get_join(a,b):
    try:
        join = Joincompany.objects.get(Q(status = "1")|Q(status="2"), id_user=a, id_company = b)
        response = {
            'id_company':b,
            'status' : join.status
        }

        return response
    except Joincompany.DoesNotExist:
        response = {
            'id_company':b,
            'status' : 'null'
        }
        return response

def get_company(b):
    try:
        join = Business.objects.get(id = b)

        response = {
            'company_name':join.company_name,
            'logo_path' : join.logo_path
        }

        return response
    except Business.DoesNotExist:
        response = {
            'company_name':'null',
            'logo_path' : 'null'}
        return response

def get_users(b):
    try:
        joinx = Register.objects.get(id = b)

        response = {
            'full_name':joinx.full_name,            
            'birth_day':joinx.birth_day
        }

        return response
    except Register.DoesNotExist:
        response = {
            'full_name':'null',            
            'birth_day':'null'}
        return response

@api_view(['GET'])
def count_emp(request,pk):
    beacon = Business.objects.get(id = pk)
    id_perusahaan = beacon.id
    nama_perusahaan = beacon.company_name
    id_admin = beacon.id_user
    nama_admin = Register.objects.get(id = id_admin).full_name
    parent_perusahaan = beacon.parent_company
    employees = Joincompany.objects.all().filter(status = "2", id_company = pk)
    counter = 0
    for man in employees :
        counter = counter+1
    total_karyawan = counter
    tabel = {
        'id_company':id_perusahaan,
        'company_name':nama_perusahaan,
        'super_admin':nama_admin,
        'parent_company':parent_perusahaan,
        'total_employees':counter
    }
    return Response(tabel)

@api_view(['GET'])
def get_ba_by_users(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    try:
        user = Register.objects.get(token = token).id
        beacon = Joincompany.objects.all().values_list('id_company', flat = True).filter(id_user = user)
        result = []
        for company in beacon: 
            try:               
                business = Business.objects.get(id = company)
                employee = Employeesign.objects.get(id_company = company, id_user = user)
                BSerializer = BusinessSerializer(business)
                ESerializer = EmployeesignSerializer(employee)
                hasil = {'Business':BSerializer.data, 'Employee_Sign': ESerializer.data}
                result.append(hasil)
            except Business.DoesNotExist:
                pass
            except Employeesign.DoesNotExist:
                pass
        return Response(result, status=status.HTTP_201_CREATED)
    except Register.DoesNotExist:
        response = {'status': 'USER DOES NOT EXIST'}
        return Response(response, status=status.HTTP_404_NOT_FOUND)


