from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import QuestTest, Testform, Testans, answ
from .serializers import QuestSerializer,TestSerializer, TestansSerializer, AnsSerializer
from registrations.models import Register
from recruitment.models import Jobs
# from recruitment.serializers import JobSerializer
# from join_company.serializers import JoincompanySerializer

from log_app.views import create_log, read_log, update_log, delete_log
from log_app.serializers import LoggingSerializer
from log_app.models import Logging
from datetime import datetime

@api_view(['POST'])
def get_post_testform(request, pk):
    if request.method == 'POST':
        try:
            beacon = request.META.get('HTTP_AUTHORIZATION')
            users = Register.objects.get(token = token)
            jobs_id = Jobs.objects.get(id = pk)
        except Jobs.DoesNotExist:
            return Response({'status' : 'Jobs Does Not Exist'}, status = status.HTTP_400_BAD_REQUEST)
        except Register.DoesNotExist:
            return Response({'status' : 'User Does Not Exist'}, status = status.HTTP_400_BAD_REQUEST)
        payloads = {
            'id_jobs' : pk,
            'serial' : datetime.now(),
            'sum_quest' : request.data['sum_quest']
        }
        serializerquest = QuestSerializer(data =payloads)
        if serializerquest.is_valid():
            serializerquest.save()
            payload = {
            'question': request.data['question'],
            'answer': request.data['answer'],
            'choose_a': request.data['choose_a'],
            'choose_b': request.data['choose_b'],
            'choose_c': request.data['choose_c'],
            'choose_d': request.data['choose_d'],
            'quest_id': serializerquest.data['id']
            }
            serializer = TestSerializer(data = payload)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.data, status = status.HTTP_400_BAD_REQUEST)
        return Response(serializerquest.data, status = status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        try:
            beacon = Testform.objects.all().filter(id_jobs = pk)
            serializer = TestSerializer(beacon, many = True)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        except Testform.DoesNotExist:
            return Response({'status':'TEST DOES NOT EXIST'}, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def get_put_delete_test(request,pk):
    try:
        beacon = Testform.objects.get(id = pk)
        if request.method == 'GET':        
            serializer = TestSerializer(beacon)        
            return Response(serializer.data, status = status)
        elif request.method == 'DELETE':
            beacon.delete()
            return Response({'status' : 'SUCCESS'}, status = status.HTTP_201_CREATED)
        elif request.method == 'PUT':
            serializer = TestSerializer(beacon, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors ,status = status.HTTP_400_BAD_REQUEST)
    except Testform.DoesNotExist:
        return Response({'status':'TEST DOES NOT EXIST'}, status = status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# def get_test_by_jobs(request,pk):
#     if request.method == 'GET':
#         try:
#             beacon = Testform.objects.all().filter(id_jobs = pk)
#             serializer = TestSerializer(beacon, many = True)
#             return Response(serializer.data, status = status.HTTP_201_CREATED)
#         except Testform.DoesNotExist:
#             return Response({'status':'TEST DOES NOT EXIST'}, status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def testans_forms(request, pk):
    token = request.META.get('HTTP_AUTHORIZATION')
    user = Register.objects.get(token = token)
    try:
        cari_soal = Testans.objects.get(id_quest = pk, id_user = user)
        return Response({'status':'Pick Another Question Set'}, status = status.HTTP_400_BAD_REQUEST)
    except Testans.DoesNotExist:
        beacon = QuestTest.objects.get(id = pk)    
        # token = request.META.get('HTTP_AUTHORIZATION')
        # user = Register.objects.get(token = token)
        payload = {
        'id_quest': beacon.id,
        'id_user': user.id
        }
        serializer = TestansSerializer(data = payload)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    except QuestTest.DoesNotExist:
        return Response({'status':'QuestTest Does Not Exist'}, status = status.HTTP_400_BAD_REQUEST)
    except Register.DoesNotExist:
        return Response({'status':'User Does Not Exist'}, status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def answer(request):
    try:
        id_testans = request.data['id_testans']
        id_test = request.data['id_test']
        answer = request.data['answer']    
        if answer == Testform.objects.get(id = id_test).answer:
            status = 1
        else:
            status = 0
        payload = {
        'id_testans' : id_testans,
        'id_test' : id_test,
        'answer' : answer,
        'status' : status
        }
        serializer = AnsSerializer(data = payload)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    except Testform.DoesNotExist:
        return Response({'status':'TestForm Does Not Exist'}, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def print_score(request, pk):
    beacon = request.META.get('HTTP_AUTHORIZATION')
    try:
        token = Register.objects.get(token = beacon)
        testanw = Testans.objects.get(id_quest = pk, id_user = token.id)
        answer = answ.objects.all().filter(id_testans = testanw.id, status = 1)
        nilai = 0
        for x in answer:
            nilai = nilai + 1
        return Response({'Your Score is' : nilai}, status = status.HTTP_201_CREATED)
    except Register.DoesNotExist:
        return Response({'status':'User Does Not Exist'}, status = status.HTTP_400_BAD_REQUEST)
    except Testans.DoesNotExist:
        return Response({'status':'User Does Not Take The Exam Yet'}, status = status.HTTP_400_BAD_REQUEST)
    except answ.DoesNotExist:
        return Response({'status':'User Does Not Complete The Exam Yet'}, status = status.HTTP_400_BAD_REQUEST)


# @api_view(['POST','GET'])
# def post_get_jobfair_by_comp(request,pk):
#     if request.method == 'POST':
#         dates = request.data['date_exp']
#         time = request.data['time_exp']
#         beacon = Jobs.objects.all().values_list('id', flat = True).filter(comp_id = pk)
#         for id_jobs in beacon:            
#             payload = {
#                 'id_comp':pk,
#                 'id_jobs':id_jobs,
#                 'date_exp':dates,
#                 'time_exp':time
#             }
#             serializer = JobfairSerializer(data = payload)
#             if serializer.is_valid():
#                 serializer.save()                
#         return Response({'status':'Transfered'}, status = status.HTTP_201_CREATED)
#     elif request.method == 'GET':
#         try: 
#             beacon = Jobfair.objects.get(id = pk)
#             netw = Jobs.objects.get(id = beacon.id_job)
#             serializer = JobSerializer(netw)
#             payload = {
#                 'id' : beacon.id,
#                 'jobs':serializer.data
#             }
#             return Response(payload, status = status.HTTP_201_CREATED)
#         except Jobs.DoesNotExist:
#             return Response({'status':'JOB DOES NOT EXIST'}, status = status.HTTP_400_BAD_REQUEST)
#         except Jobfair.DoesNotExist:
#             return Response({'status':'JOBFAIR DOES NOT EXIST'}, status = status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# def get_one_jobfair(request,pk):
#     if request.method == 'GET':
#         try:
#             beacon = Jobfair.objects.all().values_list('id_jobs', flat = True).filter(id_comp = pk)
#             lowker = []
#             for fair in beacon:
#                 jobs = Jobs.objects.get(id = fair)
#                 serializer = JobSerializer(jobs)
#                 lowker.append(serializer)
#             return Response({'status':lowker}, status = status.HTTP_201_CREATED)
#         except Jobfair.DoesNotExist:
#             return Response({'status':'JOBFAIR DOES NOT EXIST'}, status = status.HTTP_400_BAD_REQUEST)