from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import ItemCheck
from .serializers import ItemCheckSerializer


@api_view(['GET','POST'])
def get_post(request):
	if request.method == 'POST':
		serializer = ItemCheckSerializer(data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors)

	elif request.method == 'GET':
		beacon = ItemCheck.objects.all()
		serializer = ItemCheckSerializer(beacon, many = True)
		return Response(serializer.data)

@api_view(['GET','PUT','DELETE'])
def get_put_delete(request, pk):
	try:
		if request.method == 'GET':
			beacon = ItemCheck.objects.get(id = pk)
			serializer = ItemCheckSerializer(beacon)
			return Response([serializer.data])
		elif request.method == 'PUT':
			beacon = ItemCheck.objects.get(id=pk)
			serializer = ItemCheckSerializer(beacon, data = request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
			return Response(serializer.errors)
		elif request.method == 'DELETE':
			beacon = ItemCheck.objects.get(id = pk)
			beacon.delete()
			return Response({'status':'Successful !'}, status = status.HTTP_200_OK)
	except ItemCheck.DoesNotExist:
		return Response({'status':'object does not exist, are you sure the ID is correct?'}, status = status.HTTP_404_NOT_FOUND)