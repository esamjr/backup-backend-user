from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Jobfair
from .serializers import JobfairSerializer
from registrations.models import Register
from recruitment.models import Jobs
from recruitment.serializers import JobSerializer
# from join_company.serializers import JoincompanySerializer

from log_app.views import create_log, read_log, update_log, delete_log
from log_app.serializers import LoggingSerializer
from log_app.models import Logging
import time


@api_view(['POST','GET'])
def post_get_jobfair_by_comp(request,pk):
    if request.method == 'POST':
        dates = request.data['date_exp']
        time = request.data['time_exp']
        beacon = Jobs.objects.all().values_list('id', flat = True).filter(comp_id = pk)
        for id_jobs in beacon:            
            payload = {
                'id_comp':pk,
                'id_jobs':id_jobs,
                'date_exp':dates,
                'time_exp':time
            }
            serializer = JobfairSerializer(data = payload)
            if serializer.is_valid():
                serializer.save()                
        return Response({'status':'Transfered'}, status = status.HTTP_201_CREATED)
    elif request.method == 'GET':
        try: 
            beacon = Jobfair.objects.get(id = pk)
            netw = Jobs.objects.get(id = beacon.id_job)
            serializer = JobSerializer(netw)
            payload = {
                'id' : beacon.id,
                'jobs':serializer.data
            }
            return Response(payload, status = status.HTTP_201_CREATED)
        except Jobs.DoesNotExist:
            return Response({'status':'JOB DOES NOT EXIST'}, status = status.HTTP_400_BAD_REQUEST)
        except Jobfair.DoesNotExist:
            return Response({'status':'JOBFAIR DOES NOT EXIST'}, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_one_jobfair(request,pk):
    if request.method == 'GET':
        try:
            beacon = Jobfair.objects.all().values_list('id_jobs', flat = True).filter(id_comp = pk)
            lowker = []
            for fair in beacon:
                jobs = Jobs.objects.get(id = fair)
                serializer = JobSerializer(jobs)
                lowker.append(serializer)
            return Response({'status':lowker}, status = status.HTTP_201_CREATED)
        except Jobfair.DoesNotExist:
            return Response({'status':'JOBFAIR DOES NOT EXIST'}, status = status.HTTP_400_BAD_REQUEST)