from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import KPIcat
from .serializers import KPIcatSerializer


@api_view(['GET','POST'])
def get_post(request):
	if request.method == 'POST':
		serializer = KPIcatSerializer(data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors)

	elif request.method == 'GET':
		beacon = KPIcat.objects.all()
		serializer = KPIcatSerializer(beacon, many = True)
		return Response(serializer.data)

@api_view(['GET','PUT','DELETE'])
def get_put_delete(request, pk):
	try:
		if request.method == 'GET':
			beacon = KPIcat.objects.get(id = pk)
			serializer = KPIcatSerializer(beacon)
			return Response([serializer.data])
		elif request.method == 'PUT':
			beacon = KPIcat.objects.get(id=pk)
			serializer = KPIcatSerializer(beacon, data = request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
			return Response(serializer.errors)
		elif request.method == 'DELETE':
			beacon = KPIcat.objects.get(id = pk)
			beacon.delete()
			return Response({'status':'Successful !'}, status = status.HTTP_200_OK)
	except KPIcat.DoesNotExist:
		return Response({'status':'object does not exist, are you sure the ID is correct?'}, status = status.HTTP_404_NOT_FOUND)