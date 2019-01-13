from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import City as kota
from .serializers import CitySerializer

@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_city(request, pk):

    try:
        City = kota.objects.get(pk=pk)
    except City.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = CitySerializer(City)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if(request.user == City):
            City.delete()
            content = {
                'status' : 'NO CONTENT'
            }
            return Response(content, status=status.HTTP_202_NO_CONTENT)
        else:
            content = {
                'status' : 'UNAUTHORIZED'
            }
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)
    elif request.method == 'PUT':
        if(request.user == City):
            serializer = CitySerializer(user_type, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            content = {
                'status': 'UNAUTHORIZED'
            }
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET', 'POST'])
def get_post_city(request):
    if request.method == 'GET':
        network = kota.objects.all()
        serializer = CitySerializer(network, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
#@permission_classes((IsAuthenticated, ))
def get_post_region(request,pk1,pk2):
    if request.method == 'GET':
        network = kontak.objects.all().filter(id_country=pk1,id_region=pk2)
        serializer = ContactSerializer(network, many=True)
        return Response(serializer.data)