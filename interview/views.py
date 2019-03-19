from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Interview
from .serializers import InterSerializer
from registrations.models import Register

@api_view(['GET', 'DELETE',  'PUT'])
def get_put_delete_interview(request, pk):
    try: 
        beacon = Interview.objects.get(id = pk)
        if request.method == 'GET':
            serializer = InterSerializer(beacon)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            beacon.delete()
            return Response({'status':'Success Delete'}, status = status.HTTP_204_NO_CONTENT)
        elif request.method == 'PUT':
            serializer = InterSerializer(beacon, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    except Interview.DoesNotExist:
        return Response({'status':'Interview Schedule Does Not Exist'}, status = status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def get_post_interview(request):
    if request.method == 'GET':
        network = Interview.objects.all()
        serializer = InterSerializer(network, many=True)
        return Response(serializer.data, status = status.HTTP_201_CREATED)

    elif request.method == 'POST':
        serializer = InterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
