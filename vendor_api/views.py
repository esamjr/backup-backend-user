from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Vendor_api
from .serializers import VendorSerializer
from registrations.serializers import TokenSerializer
from django.contrib.auth.hashers import check_password, make_password, is_password_usable
from registrations.models import Register, Domoo
from registrations.serializers import DomoSerializer
from registrations.views import attempt_login, forget_attempt
from join_company.models import Joincompany
from business_account.models import Business
from hierarchy.models import Hierarchy
from license_company.models import LicenseComp
from django.conf import settings
import requests
import json
import datetime
import time

@api_view(['GET'])
def search_by_token(request, stri):	
	try:
		token = requests.META.get('HTTP_AUTHORIZATION')
		user = Register.objects.get(token = token)
		if stri == 'admincompany':			
			admins = Business.objects.all().values_list('id', flat = True).filter(id_user = user.id)
			result = []
			for id_comp in admins:
				company = Business.objects.get(id = id_comp)
				payload = {
				'id':company.id,
				'name':company.company_name,
				'logo':company.logo_path,
				'parent_company':company.parent_company,
				'email':company.email
				}
				result.append(payload)
			return Response(result, status = status.HTTP_200_OK)

		elif stri == 'usertoken':
			payload = {
			'id': user.id,
			'fullname':user.full_name,
			'token': user.token
			}
			return Response(payload, status = status.HTTP_200_OK)

		elif stri == 'join_company':
			joins = Joincompany.objects.all().values_list('id', flat = True).filter(id_user = user.id, status = '2')
			result = []
			for join in joins:
				beacon = Joincompany.objects.get(id = join)
				payload = {
				'id':beacon.id,
				'id_company':beacon.id_company,
				'id_rec':beacon.id_rec
				}
				result.append(payload)
			return Response(result, status = status.HTTP_200_OK)
		else:
			return Response({'status':'The URL is Invalid, Please Check Again'}, status = status.HTTP_400_BAD_REQUEST)

	except Register.DoesNotExist:
		return Response({'status': 'Your Credential is Invalid, Please Login Again'}, status = status.HTTP_401_UNAUTHORIZED)
	except Business.DoesNotExist:
		return Response({'status': 'You are not an admin company'}, status = status.HTTP_401_UNAUTHORIZED)
	except Joincompany.DoesNotExist:
		return Response({'status': 'You dont have any employer'}, status = status.HTTP_200_OK)

@api_view(['GET'])
def api_payroll(request, pk):
	if request.method == 'GET':
		try:
			token = request.META.get('HTTP_AUTHORIZATION')
			IsAdmin = Register.objects.get(token = token)
			# comp = Business.objects.get(id_user = IsAdmin.id, id = pk)
			hierarki = Hierarchy.objects.get(id_company = pk, id_user = IsAdmin.id)
			license = LicenseComp.objects.get(id_comp = pk, status = '1', id_hierarchy = hierarki.id)
			if license.payroll == '2':
				state = 'IsAdmin'
			elif license.payroll == '1':
				state = 'IsUser'
			else:
				state = 'IsNothing'

			payload = {
			'status': state,
			'id_comp': pk
			}
			return Response(payload, status = status.HTTP_200_OK)
		except Register.DoesNotExist:
			return Response({'status':'User is not exist.'}, status = status.HTTP_401_UNAUTHORIZED)
		except Business.DoesNotExist:
			return Response({'status':'User is not admin company.'}, status = status.HTTP_401_UNAUTHORIZED)
		except Hierarchy.DoesNotExist:
			return Response({'status':'User is not in Hierarchy company.'}, status = status.HTTP_401_UNAUTHORIZED)
		except LicenseComp.DoesNotExist:
			return Response({'status':'User is not Registered in License company.'}, status = status.HTTP_401_UNAUTHORIZED)

@api_view(['GET', 'POST', 'DELETE'])
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

	elif request.method == 'DELETE':
		token = request.META.get('HTTP_AUTHORIZATION')
		try:
			user = Register.objects.get(token = token)		
			if user.id == 0:
				comp_token = request.data['token_comp']			
				comp = Vendor_api.objects.get(token = comp_token)
				comp.delete()
				return Response({'status':'Deleted'}, status = status.HTTP_204_NO_CONTENT)			
			else:
				return Response({'status':'Hold up, you are not authorized to access this'}, status = status.HTTP_401_UNAUTHORIZED)
		except Vendor_api.DoesNotExist:
			return Response({'status':'Vendor Not Found'}, status = status.HTTP_404_NOT_FOUND)
		except Register.DoesNotExist:
			return Response({'status':'YOU DONT HAVE ACCESS.'}, status = status.HTTP_400_BAD_REQUEST)

	elif request.method == 'GET':
		try:
			token = request.META.get('HTTP_AUTHORIZATION')
			user = Register.objects.get(token = token)
			if user.id == 0:
				network = Vendor_api.objects.all()
				serializer = VendorSerializer(network, many=True)
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			else:
				return Response({'status':'YOU DONT HAVE ACCESS'}, status = status.HTTP_401_UNAUTHORIZED)
		except Register.DoesNotExist:
			return Response({'status':'YOU ARE NOTHING.'}, status = status.HTTP_400_BAD_REQUEST)

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

@api_view(['POST', 'PUT'])
def api_login_absensee_v2(request, pk):	
	try:
		if request.method == 'POST':
			token_vendor = request.META.get('HTTP_AUTHORIZATION')
			if token_vendor == 'xxx':
				return Response({'status':'Vendor Token, is Unauthorized.'}, status = status.HTTP_401_UNAUTHORIZED)		
			vendor = Vendor_api.objects.get(token = token_vendor)

			email = request.data['email']
			password = request.data['password']

			#------------------tambahan ----------------------
			# token = request.META.get('HTTP_AUTHORIZATION')
			user = Register.objects.get(email = email)
			comp = Business.objects.get(id_user = user.id, id = pk)
			hierarki = Hierarchy.objects.get(id_company = comp.id, id_user = user.id)
			license = LicenseComp.objects.get(id_comp = comp.id, status = '1', id_hierarchy = hierarki.id)
			sekarang = datetime.datetime.now().date()
			
			if license.expr_date >= sekarang:
				masa = 'Masih bisa'
			else:
				return Response({'status':'udah expired'}, status = status.HTTP_401_UNAUTHORIZED)
			
			if vendor.username == 'Absensee':
				if license.attendance == '1':
					state = 'IsAdmin'
				elif license.attendance == '2':
					state = 'IsUser'
				else:
					state = 'IsNothing'
					
			elif vendor.username == 'ERP':
				if license.attendance == '1':
					state = 'IsAdmin'
				elif license.attendance == '2':
					state = 'IsUser'
				else:
					state = 'IsNothing'
					
			elif vendor.username == 'payroll':					
				if license.payroll == '1':
					state = 'IsAdmin'
				elif license.payroll == '2':
					state = 'IsUser'
				else:
					state = 'IsNothing'

				payload = {
				'token':user.token,
				'status': state,
				'id_comp': comp.id,
				'masa':masa
				}
				return Response(payload, status = status.HTTP_200_OK)
			else:
				return Response({'status':'Vendor Belum Terintegrasi Dengan Mindzzle'})	

				
			#---------------------------------------------------------

			user = Register.objects.get(email = email)
			attempt = user.attempt
			salt = user.full_name
			salt_password = ''.join(str(ord(c)) for c in salt)
			thepassword = password + salt_password

			if (check_password(thepassword, user.password)):			
				token = make_password(str(time.time()))
				payload = {'token':token}
				serializer = TokenSerializer(user, data = payload)
				#----------------------TESTING (tambahan v2)----------------------
				if serializer.is_valid():
					serializer.save()
					beacon = Business.objects.get(id = pk)
					payload = {
					'token_user': user.token,
					'image': beacon.logo_path,
					'comp_id': beacon.id,
					'comp_name': beacon.company_name,
					'masa':masa
					}
					return Response(payload, status = status.HTTP_200_OK)
				return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
				#---------------------------------------------------
				# if serializer.is_valid():
				# 	serializer.save()
				# 	companies = Joincompany.objects.all().values_list('id_company', flat = True).filter(id_user = user.id, status = '2')
				# 	comp = []
				# 	for company in companies:
				# 		beacon = Business.objects.get(id = company)
				# 		payload = {
				# 		'token_user': user.token,
				# 		'image': beacon.logo_path,
				# 		'comp_id': beacon.id,
				# 		'comp_name': beacon.company_name
				# 		}
				# 		comp.append(payload)
				# 	return Response(comp, status = status.HTTP_201_CREATED)
				# else:
				# 	return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)
			else: 
				if (attempt == 0):
					attempt_login(request, email)
					response = {'status' : 'Wrong Username / Password'}
					return Response(response, status=status.HTTP_400_BAD_REQUEST)
				elif(attempt % 5 == 0):
					forget_attempt(request, email)
					return Response(forget_attempt, status=status.HTTP_401_UNAUTHORIZED)
				else:
					attempt_login(request, email)
					response = {'status' : 'Wrong Username / Password'}
					return Response(response, status=status.HTTP_400_BAD_REQUEST)
			# return Response({'status':'Invalid Username or Password'}, status = status.HTTP_401_UNAUTHORIZED)
		elif request.method == 'PUT':
			token_vendor = 	request.META.get('HTTP_AUTHORIZATION')
			token_user = request.data['token_user']
			vendor = Vendor_api.objects.get(token = token_vendor)
			user = Register.objects.get(token = token_user)
			payload = {'token':'xxx'}
			serializer = TokenSerializer(user, data = payload)
			if serializer.is_valid():
				serializer.save()
				return Response({'status':'User Has Logout'}, status = status.HTTP_200_OK)
			return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

	except Vendor_api.DoesNotExist:
		return Response({'status':'Vendor Token, is Does Not Exist.'}, status = status.HTTP_401_UNAUTHORIZED)
	except Register.DoesNotExist:
		return Response({'status':'User is Unauthorized.'}, status = status.HTTP_401_UNAUTHORIZED)
	except Joincompany.DoesNotExist:
		return Response({'status':'User did not have any company'}, status = status.HTTP_202_ACCEPTED)
	except Business.DoesNotExist:
		return Response({'status':'The Company Does Not Exist'}, status = status.HTTP_202_ACCEPTED)
	except Hierarchy.DoesNotExist:
		return Response({'status':'User is not in Hierarchy company.'}, status = status.HTTP_401_UNAUTHORIZED)
	except LicenseComp.DoesNotExist:
		return Response({'status':'User is not Registered in License company.'}, status = status.HTTP_401_UNAUTHORIZED)


@api_view(['POST', 'GET'])
def api_login_absensee(request):	
	try:
		if request.method == 'POST':
			token_vendor = request.META.get('HTTP_AUTHORIZATION')
			if token_vendor == 'xxx':
				return Response({'status':'Vendor Token, is Unauthorized.'}, status = status.HTTP_401_UNAUTHORIZED)		
			vendor = Vendor_api.objects.get(token = token_vendor)

			email = request.data['email']
			password = request.data['password']			
			user = Register.objects.get(email = email)
			attempt = user.attempt
			salt = user.full_name
			salt_password = ''.join(str(ord(c)) for c in salt)
			thepassword = password + salt_password

			if (check_password(thepassword, user.password)):			
				token = make_password(str(time.time()))
				payload = {'token':token}
				serializer = TokenSerializer(user, data = payload)
				if serializer.is_valid():
					serializer.save()
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

					profil = {
					'id':user.id,
					'name':user.full_name,
					'photo':user.url_photo
					}

					payloads = {
						'api_status':1,
						'api_message':'success',
						'profile': profil,
						'companies':comp
					}
					# payloads = {
					# 	'nama':"['api_status'=>1,'api_message'=>'success','profile'=>{'id'=>1,'name'=>"+user.full_name+",'photo'=>"+user.url_photo+"}'companies'=>"+str(comp)+"]"
					# }
					

					return Response(payloads, status = status.HTTP_201_CREATED)

				else:
					return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)
			else: 
				if (attempt == 0):
					attempt_login(request, email)
					response = {'status' : 'Wrong Username / Password'}
					return Response(response, status=status.HTTP_400_BAD_REQUEST)
				elif(attempt % 5 == 0):
					forget_attempt(request, email)
					return Response(forget_attempt, status=status.HTTP_401_UNAUTHORIZED)
				else:
					attempt_login(request, email)
					response = {'status' : 'Wrong Username / Password'}
					return Response(response, status=status.HTTP_400_BAD_REQUEST)
			# return Response({'status':'Invalid Username or Password'}, status = status.HTTP_401_UNAUTHORIZED)
		elif request.method == 'GET':
			token_vendor = 	request.META.get('HTTP_AUTHORIZATION')
			token_user = request.data['token_user']
			vendor = Vendor_api.objects.get(token = token_vendor)
			user = Register.objects.get(token = token_user)
			payload = {'token':'xxx'}
			serializer = TokenSerializer(user, data = payload)
			if serializer.is_valid():
				serializer.save()
				return Response({'status':'User Has Logout'}, status = status.HTTP_200_OK)
			return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

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
			auth = 'IsUser'
		elif license.attendance == '2':
			auth = 'IsAdmin'
		else:
			return Response({'status':'User is Unauthorized to Attendance.'}, status = status.HTTP_401_UNAUTHORIZED)
		payload = {
		'fullname': user.full_name,
		'division': hierarchy.division,
		'company_name': company.company_name,
		'client_auth': auth,
		'client_token' : user.token
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

@api_view(['PUT'])
def change_status_domoo_user(request):
	try:
		token = request.META.get('HTTP_AUTHORIZATION')
		user = Register.objects.get(token = token)
		beacon = Domoo.objects.get(pk=user.id)
		stat = request.data['status']
		payload = {
		'id_user':pk,
		'status': stat
		}
		seralizer = DomoSerializer(beacon, data = payload)
		if seralizer.is_valid():
			seralizer.save()
			return Response(seralizer.data, status = status.HTTP_201_CREATED)
		return Response(seralizer.errors, status = status.HTTP_400_BAD_REQUEST)
	except Domoo.DoesNotExist:
		return Response({'status': 'Not Domoo User'})

@api_view(['POST'])
def check_user_domoo(request):
	if request.method == 'POST':

		if settings.DEBUG == False:
			url = 'http://api-staging.doomo.id/customers/infocustomer'
		elif settings.DEBUG == True:
			url = 'http://api-staging.doomo.id/customers/infocustomer'

		phnoe = request.data['phone']
		r = requests.post(url, data = {'mobile': phnoe}, headers = {'Accept': 'application/pasy.v1+json'})
		data = r.json()
		try:
			cust = data['customers']
			# return Response(cust)
			if cust['status'] == '0':
				# beacon = 
				return Response({'status':'Silahkan verifikasi akun Domoo anda', 'Balance':cust['balance'],'Benefit':cust['benefit']}, status = status.HTTP_200_OK)
			elif cust['status'] == '1':
				return Response({'status':'1','Balance':cust['balance'],'Benefit':cust['benefit']}, status = status.HTTP_200_OK)			
		except Exception:
			return Response(data, status = status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def registrations_domoo(request):
	if settings.FLAG == 1:
		url = 'http://api-staging.doomo.id/customers'
	elif settings.FLAG == 0:
		url = 'http://api-staging.doomo.id/customers'

	email = request.data['email']
	payload = {
	'name': request.data['name'],
	'mobile' : request.data['phone'],
	'email': email
	}

	Req = requests.post(url, data = payload, headers = {'Accept': 'application/pasy.v1+json'})
	Res = Req.json()
	try:
		resp = Res['customers']
		try:
			user = Register.objects.get(email = email)
			beacon = Domoo.objects.get(pk=user.id)
			stat = 1
			payload = {
			'id_user':user.id,
			'status': stat
			}
			seralizer = DomoSerializer(beacon, data = payload)
			if seralizer.is_valid():
				seralizer.save()
				return Response(seralizer.data, status = status.HTTP_201_CREATED)
			return Response(seralizer.errors, status = status.HTTP_400_BAD_REQUEST)
		except Domoo.DoesNotExist:
			return Response({'status': 'Not Domoo User'})
		return Response(resp, status = status.HTTP_200_OK)
	except Exception:
		resp = Res['message']
		return Response(resp, status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def verify_otp_domoo(request):
	if settings.FLAG == 1:
		url = 'http://api-staging.doomo.id/customers/verify'
	elif settings.FLAG == 0:
		url = 'http://api-staging.doomo.id/customers/verify'
	payload = {
	'mobile': request.data['phone'],
	'code': request.data['otp']
	}
	req = requests.post(url, data = payload, headers= {'Accept': 'application/pasy.v1+json'})
	Res = req.json()
	try:
		resp = Res['customers']
		return Response(resp, status = status.HTTP_200_OK)
	except Exception:
		resp = Res['message']
		return Response(resp, status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def set_passcode_domoo(request):
	if settings.FLAG == 1:
		url = 'http://api-staging.doomo.id/customers/passcode'
	elif settings.FLAG == 0:
		url = 'http://api-staging.doomo.id/customers/passcode'

	payload  = {
	'passcode': request.data['password'],
	'passcode_confirmation': request.data['confirmation']
	}

	headers = {
	'Accept': 'application/pasy.v1+json',
	'AccessToken': request.data['token_domoo']
	}

	Req = requests.put(url, data = payload, headers = headers)
	Res = Req.json()

	token = request.META.get('HTTP_AUTHORIZATION')
	user = Register.objects.get(token = token)
	domo = Domoo.objects.get(id_user = user.id)
	payload = {
	'id_user':user.id,
	'status':2
	}
	serializerdomo = DomoSerializer(domo, data = payload)
	if serializerdomo.is_valid():
		serializerdomo.save()

	return Response(Res['message'])

@api_view(['POST'])
def forget_passcode_domoo(request):
	if settings.FLAG == 1:
		url = 'http://api-staging.doomo.id/customers/passcode/'
	elif settings.FLAG == 0:
		url = 'http://api-staging.doomo.id/customers/passcode/'

	phone = request.data['phone']
	headers = {
	'Accept': 'application/pasy.v1+json'
	}
	Req = requests.get(url+str(phone), headers = headers)
	Res = Req.json()
	return Response(Res['message'])

@api_view(['POST','PUT'])
def login_logout_domoo(request):
	if request.method == 'POST':
		if settings.FLAG == 1:
			url = 'http://api-staging.doomo.id/customers/auth?'
		elif settings.FLAG == 0:
			url = 'http://api-staging.doomo.id/customers/auth?'

		payload = {
		'mobile': request.data['phone'],
		'passcode' : request.data['password']
		# 'device_active'
		}

		headers = {
		'Accept': 'application/pasy.v1+json'
		}

		Req = requests.post(url, data = payload, headers = headers)
		Res = Req.json()

		try:
			resp = Res['customers']
			token = resp['access_token']
			return Response(resp, status = status.HTTP_202_ACCEPTED)
		except Exception:
			resp = Res['message']
			return Response(resp, status = status.HTTP_401_UNAUTHORIZED)

	elif request.method == 'PUT':
		if settings.FLAG == 1:
			url = 'http://api-staging.doomo.id/customers/auth?'
		elif settings.FLAG == 0:
			url = 'http://api-staging.doomo.id/customers/auth?'

			token = request.data['token']		

			headers = {
			'Accept': 'application/pasy.v1+json',
			'AccessToken': token
			}

			Req = requests.put(url, headers = headers)
			Res = Req.json()
			return Response(Res['message'])
