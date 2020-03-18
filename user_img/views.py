from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from OCR_Reader.serializers import UserImgSerializer
from registrations.models import Register
from registrations.helper import _cek_user

from .models import User_img
from .serializers import ValidSerializer, ExpTaxnumSerializer


@api_view(['GET'])
def get_all_doc(request):
    """'
    API endpoint for get npwp and ktp order by id_user
    """
    try:
        _user = _cek_user(request.query_params['id_user'])
        data = User_img.objects.filter(id_user=_user.id).values()
        result = []
        for i in data:
            payload = {
                'id': i['id'],
                'id_user': i['id_user'],
                'type_name': i['type_name'],
                'url_ktp': i['url_ktp'],
                'no_ktp': i['no_ktp'],
                'url_npwp': i['url_npwp'],
                'no_npwp': i['no_npwp'],
            }
            result.append(payload)

        response = {
            'api_status': status.HTTP_200_OK,
            'api_message': "documents user bisa diambil",
            'data': result
        }

        return JsonResponse(response)

    except Exception as ex:
        response = {
            'api_error': status.HTTP_400_BAD_REQUEST,
            'api_status': str(ex.args)
        }

        return JsonResponse(response)

@api_view(['GET','PUT'])
def get_doc(request):
	token = request.META.get('HTTP_AUTHORIZATION')
	if request.method == 'GET':
		try:
			user = Register.objects.get(token = token).id
			datas = User_img.objects.get(id_user = user)
			serializer = UserImgSerializer(datas)
			return Response(serializer.data, status = status.HTTP_200_OK)
		except Register.DoesNotExist:
			return Response({'status':'YOU DID NOT HAVE ACCESS'}, status = status.HTTP_401_UNAUTHORIZED)
		except User_img.DoesNotExist:
			return Response({'status':'YOUR DATA IS NOT AVAILABLE'}, status = status.HTTP_400_BAD_REQUEST)
	elif request.method == 'PUT':
		try:
			user = Register.objects.get(token = token).id
			print('user: ' + str(user))
			datas = User_img.objects.get(id_user = user)
			serializer = UserImgSerializer(datas, data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status = status.HTTP_200_OK)
			return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
		except Register.DoesNotExist:
			return Response({'status':'YOU DID NOT HAVE ACCESS'}, status = status.HTTP_401_UNAUTHORIZED)
		except User_img.DoesNotExist:
			return Response({'status':'YOUR DATA IS NOT AVAILABLE'}, status = status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def upload_doc(request):	
	try:
		get_token = request.META.get('HTTP_AUTHORIZATION')
		token = Register.objects.get(token = get_token).id
		user = Register.objects.get(token = get_token)
		type_name = request.data['type_name']
		url = request.data['url']
		nomor = request.data['nomor']
		
		if (type_name == "ktp"):
			payload = {
				'id_user' : token,
				'type_name' : type_name,
				'no_ktp' : nomor,
				'url_ktp' : url,
				'status' : "1"}			
			serializers = UserImgSerializer(data = payload)
			if serializers.is_valid():			
				serializers.save()
				payloads = {'ssn_num':nomor,
							'verfied':"1"}
				serializer2 = ValidSerializer(user, data = payloads)
				if serializer2.is_valid():
					serializer2.save()
					response = {'status' : 'OK'}
					return Response(response, status = status.HTTP_201_CREATED)
				return Response(serializer2.errors, status = status.HTTP_400_BAD_REQUEST)
			return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)
			
		elif (type_name == "npwp"):
			beacon = User_img.objects.get(id_user = token)
			payload = {
				'id_user' : token,
				'type_name' : type_name,
				'no_npwp' : nomor,
				'url_npwp' : url,
				'no_ktp' : beacon.no_ktp,
				'url_ktp' : beacon.url_ktp
				}
			serializers = UserImgSerializer(beacon, data = payload)
			if serializers.is_valid():
				serializers.save()
				payloads = {'tax_num': nomor}
				serializer2 = ExpTaxnumSerializer(user, data = payloads)
				if serializer2.is_valid():
					serializer2.save()
					response = {'status' : 'OK'}
					return Response(response, status = status.HTTP_201_CREATED)
				return Response(serializer2.errors, status = status.HTTP_400_BAD_REQUEST)
			return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)
	except Register.DoesNotExist:
		response = {'status' : 'Register Does Not Exist'}
		return Response(response, status = status.HTTP_401_UNAUTHORIZED)


