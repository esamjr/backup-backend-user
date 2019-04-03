from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Vendor_api
from rest_framework_jwt.settings import api_settings
from .serializers import VendorSerializer
from django.contrib.auth.hashers import check_password, make_password, is_password_usable
from registrations.models import Register
from join_company.models import Joincompany
from business_account.models import Business
from hierarchy.models import Hierarchy
from license_company.models import LicenseComp

@api_view(['GET', 'POST'])
def generate(request):
	if request.method == 'POST':
		# jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
		# jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

		vendor = request.data['vendors']
		username = request.data['username']
		password = request.data['password']
		hashes = ''.join(str(ord(c))for c in vendor)

		# payload = jwt_payload_handler(username)
		# token = jwt_encode_handler(payload)
		# token = request.data['token']

		payloads = {
			'username' : username,
			'password' : make_password(str(hashes) + str(password)),
			'vendor_name' : vendor,
			'token' : make_password(str(hashes) + 'Mind55L3')
		}
		serializer = VendorSerializer(data = payloads)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	elif request.method == 'GET':
		try:
			token = request.META.get('HTTP_AUTHORIZATION')
			user = Register.objects.get(token = token)
			if user.id == '0':
				network = Vendor_api.objects.all()
				serializer = VendorSerializer(network, many=True)
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			else:
				return Response({'status':'YOU DONT HAVE ACCESS'}, status = status.HTTP_401_UNAUTHORIZED)
		except Register.DoesNotExist:
			return Response({'status':'YOU DONT HAVE ACCESS.'}, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def login_logout_vendors(request):
	if request.method == 'POST':
		try:
			username = request.data['username']
			password = request.data['password']
			beacon = Vendor_api.objects.get(username = username)
			hashes = ''.join(str(ord(c))for c in beacon.vendor_name)
			key = hashes + password
			if (check_password(key , beacon.password)):
				payloads = {
					'username' : username,
					'password' : make_password(str(hashes) + str(password)),
					'vendor_name' : beacon.vendor_name,
					'token' : make_password(str(hashes) + 'Mind55L3')
				}
				serializer = VendorSerializer(beacon,data = payloads)
				if serializer.is_valid():
					serializer.save()
					return Response( serializer.data, status = status.HTTP_202_ACCEPTED)
				return Response( serializer.errors, status = status.HTTP_400_BAD_REQUEST)
			else:
				return Response({'status':'wrong username / password'}, status = status.HTTP_401_UNAUTHORIZED)
		except Vendor_api.DoesNotExist:
			return Response({'status':'YOU DONT HAVE ACCESS.'}, status = status.HTTP_400_BAD_REQUEST)
	elif request.method == 'GET':
		try:
			token = request.META.get('HTTP_AUTHORIZATION')
			beacon = Vendor_api.objects.get(token = token)
			payload = {
				'username': beacon.username,
				'password': beacon.password,
				'vendor_name': beacon.vendor_name,
				'token': 'xxx'
				}
			serializer = VendorSerializer(beacon, data = payload)
			if serializer.is_valid():
				serializer.save()
				return Response({'status':'YOU HAS LOGOUT'}, status = status.HTTP_202_ACCEPTED)
			return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
		except Vendor_api.DoesNotExist:
			return Response({'status':'YOU MOST LOGIN FIRST.'}, status = status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def api_login_absensee(request):	
	try:
		token_vendor = request.META.get('HTTP_AUTHORIZATION')
		if token_vendor == 'xxx':
			return Response({'status':'Vendor Token, is Unauthorized.'}, status = status.HTTP_401_UNAUTHORIZED)		
		vendor = Vendor_api.objects.get(token = token_vendor)

		email = request.data['email']
		password = request.data['password']
		user = Register.objects.get(email = email)
		companies = Joincompany.objects.all().values_list('id_company', flat = True).filter(id_user = user.id, status = '2')
		comp = []
		for company in companies:
			beacon = Business.objects.get(id = company)
			payload = {
			'token_user': user.token,
			'image': beacon.logo_path,
			'comp_id': beacon.id,
			'comp_name': beacon.company_name
			}
			comp.append(payload)
		return Response(comp, status = status.HTTP_201_CREATED)

	except Vendor_api.DoesNotExist:
		return Response({'status':'Vendor Token, is Unauthorized.'}, status = status.HTTP_401_UNAUTHORIZED)
	except Register.DoesNotExist:
		return Response({'status':'User is Unauthorized.'}, status = status.HTTP_401_UNAUTHORIZED)
	except Joincompany.DoesNotExist:
		return Response({'status':'User did not have any company'}, status = status.HTTP_202_ACCEPTED)
	except Business.DoesNotExist:
		return Response({'status':'The Company Does Not Exist'}, status = status.HTTP_202_ACCEPTED)

@api_view(['GET'])
def api_find_company_absensee(request):
	try:
		token_vendor = request.META.get('HTTP_AUTHORIZATION')
		vendor = Vendor_api.objects.get(token = token_vendor)
		token = request.data['token_user']
		id_comp = request.data['id_comp']
		user = Register.objects.get(token = token)
		company = Business.objects.get(id = id_comp)
		hierarchy = Hierarchy.objects.get(id_user = user.id, id_company = id_comp)
		license = LicenseComp.objects.get(id_hierarchy = hierarchy.id, id_comp = hierarchy.id_company)
		if license.attendance == '1':
			auth = 'IsAdmin'
		elif license.attendance == '2':
			auth = 'IsUser'
		else:
			return Response({'status':'User is Unauthorized to Attendance.'}, status = status.HTTP_401_UNAUTHORIZED)
		payload = {
		'fullname': user.full_name,
		'division': hierarchy.division,
		'company_name': company.company_name,
		'absensee_auth': auth
		}
		return Response(payload, status = status.HTTP_202_ACCEPTED)
	except Vendor_api.DoesNotExist:
		return Response({'status':'Vendor Token, is Unauthorized.'}, status = status.HTTP_401_UNAUTHORIZED)
	except Register.DoesNotExist:
		return Response({'status':'User is Unauthorized.'}, status = status.HTTP_401_UNAUTHORIZED)
	except Hierarchy.DoesNotExist:
		return Response({'status':'User did not have any relation in the company'}, status = status.HTTP_202_ACCEPTED)
	except Business.DoesNotExist:
		return Response({'status':'The Company Does Not Exist'}, status = status.HTTP_202_ACCEPTED)
