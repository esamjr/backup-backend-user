from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import AwardBA
from businness_account.models import Business
from registrations.models import Register
from .serializers import AwardBASerializer

from log_app.views import create_log, read_log, update_log, delete_log
from log_app.serializers import LoggingSerializer
from log_app.models import Logging
import time

@api_view(['GET','DELETE', 'PUT'])
def get_delete_update_award(request, pk):
   try:
       token = request.META.get('HTTP_AUTHORIZATION')
       get_token = Register.objects.get(token = token).id
       admin = Business.objects.get(id_user = get_token)
       awards = AwardBA.objects.get(pk = pk)
        if request.method == 'GET':
            serializer = AwardBASerializer(awards)
            act = 'Read Award BA by '                           
            read_log(request, get_token, act)
            return Response(serializer.data)

        elif request.method == 'DELETE':
            act = 'Delete award by id : '                           
            read_log(request, get_token, act)                                         
            awards.delete()
            content = {
                'status' : 'NO CONTENT'
            }
            return Response(content, status=status.HTTP_204_NO_CONTENT)

        elif request.method == 'PUT':
            serializer = AwardBASerializer(awards, data=request.data)
            if serializer.is_valid():
                act = 'Update certification by '
                update_log(request, get_token, act)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Register.DoesNotExist: 
        return Response({'status':'User Does Not Exist '}, status = status.HTTP_400_BAD_REQUEST)           
    except AwardBA.DoesNotExist: 
        return Response({'status':'Award Does Not Exist '}, status = status.HTTP_400_BAD_REQUEST)       
    except Business.DoesNotExist: 
        return Response({'status':'YOU ARE NOT THE ONE'}, status = status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'POST'])
def get_post_award(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    registrations = Register.objects.get(token =token)
    if request.method == 'GET':
        network = AwardBA.objects.all()
        serializer = AwardBASerializer(network, many=True)
        act = 'Read all award BA by '                           
        read_log(request, registrations, act)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AwardBASerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            act = 'Create new award by '
            create_log(request, registrations, act)                
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

