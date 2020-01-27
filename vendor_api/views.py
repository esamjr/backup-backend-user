import csv
import datetime
import time
from random import randint

import requests
from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import EmailMessage
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from business_account.models import Business
from business_account.serializers import BusinessSerializer
from email_app.views import multidevices_email, vendors_login_alert
from hierarchy.models import Hierarchy
from hierarchy.serializers import HierarchySerializer
from join_company.models import Joincompany
from license_company.models import LicenseComp
from log_app.views import read_log
from registrations.models import Register
from registrations.serializers import forgetblastSerializer
from registrations.views import attempt_login, forget_attempt
from .models import Vendor_api, MultipleLogin
from .serializers import VendorSerializer, MultipleSerializer
from registrations.models import Register


@api_view(['GET'])
def search_by_token(request, stri):	
	try:
		token = request.META.get('HTTP_AUTHORIZATION')
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
#-----------------------------------------------BILLING API------------------------------------------------------------

@api_view(['GET'])
def sync_billing(request):
	try:
		token = request.META.get('HTTP_AUTHORIZATION')
		admin = Register.objects.get(token = token)
		if admin.id != 0:
			return Response({'status':'User Is Not Super Admin, Please contact Mindzzle Backend'}, status = status.HTTP_400_BAD_REQUEST)
		elif admin.id == 0:
			bisnis = Business.objects.all().values_list('id' , 'id_user').filter(banned_type = 2)
			result = []
			for id_biz, id_use in bisnis:
				beaconbiz = Business.objects.get(id = id_biz)
				bizser = BusinessSerializer(beaconbiz)
				bizadm = Register.objects.get(id = id_use)
				payload = {
				'Business':bizser.data,
				'Superadmin' : {'name' : bizadm.full_name, 'email':bizadm.email}
				}
				result.append(payload)
			return Response(result, status = status.HTTP_200_OK)
		else:
			return Response({'status':'User did not have credentials'}, status = status.HTTP_401_UNAUTHORIZED)
	except Register.DoesNotExist:
		return Response({'status':'User Did Not Exist'}, status = status.HTTP_404_NOT_FOUND)

#-----------------------------------------------PAYROLL API-----------------------------------------------------------------------------------
@api_view(['GET'])
def sync_emp_config(request):
	if request.method == 'GET':
		try:
			token = request.META.get('HTTP_AUTHORIZATION')
			comp = request.data['comp_id']
			user = Register.objects.get(token = token)
			company = Business.objects.get(id_user = user.id, id = comp)
			hierarchy_comp = Hierarchy.objects.all().values_list('id', flat = True).filter(id_company = company.id)
			return Response({'result':hierarchy_comp}, status = status.HTTP_200_OK)
		except Register.DoesNotExist:
			return Response({'status':'You Must Login First'}, status = status.HTTP_401_UNAUTHORIZED)
		except Business.DoesNotExist:
			return Response({'status':'ID Company is Did not match'}, status = status.HTTP_404_NOT_FOUND)
		except Hierarchy.DoesNotExist:
			return Response({'status':'Hierarchy is Empty, fill The company hierarchy first'})

@api_view(['GET'])
def check_hierarchy(request,pk):
	beacon = Hierarchy.objects.all().filter(id_company = pk)
	serializer = HierarchySerializer(beacon, many = True)
	return Response(serializer.data)


@api_view(['GET'])
def api_payroll(request, pk):
		try:
			_admins = Register.objects.get(id=pk)
			comp = Business.objects.get(id = pk)
			hierarki = Hierarchy.objects.get(id_company=pk, id_user=_admins.id)
			license = LicenseComp.objects.get(id_comp=pk, status='1', id_hierarchy=hierarki.id)
			if license.payroll == '2':
				state = 'IsAdmin'
				payload = {
					'status': state,
					'email': comp.email,
					'name': comp.company_name,
					'logo': comp.logo_path,
				}
				return Response(payload, status=status.HTTP_200_OK)

			elif license.payroll == '1':
				state = 'IsUser'
			else:
				state = 'IsNothing'

			payload = {
				'status': state,
				'id_comp': pk
			}
			return Response(payload, status=status.HTTP_200_OK)
		except Register.DoesNotExist:
			return Response({'status':'User is not exist.'}, status=status.HTTP_401_UNAUTHORIZED)
		except Business.DoesNotExist:
			return Response({'status':'User is not admin company.'}, status=status.HTTP_401_UNAUTHORIZED)
		except Hierarchy.DoesNotExist:
			return Response({'status':'User is not in Hierarchy company.'}, status=status.HTTP_401_UNAUTHORIZED)
		except LicenseComp.DoesNotExist:
			return Response({'status':'User is not Registered in License company.'}, status=status.HTTP_401_UNAUTHORIZED)


#-----------------------------------------------------REGISTER THIRD PARTY API------------------------------------------------------------------
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

#------------------------------------------------GENERAL API--------------------------------------------------------------------------------------------
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
					vendors = serializer.data['vendor_name']
					vendors_login_alert(request,vendors)
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
				vendors = beacon.vendor_name
				vendors_login_alert(request,vendors)
				return Response({'status':'YOU HAS LOGOUT'}, status = status.HTTP_202_ACCEPTED)
			return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
			
		except Vendor_api.DoesNotExist:
			return Response({'status':'YOU MOST LOGIN FIRST.'}, status = status.HTTP_401_UNAUTHORIZED)

def ERP_token_generator():
	range_start = 10**(6-1)
	range_end = (10**6)-1
	return randint(range_start,range_end)

@api_view(['POST', 'PUT', 'GET'])
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
			
			if datetime.datetime.strptime(str(license.expr_date), '%Y-%m-%d').date() >= sekarang:
				masa = 'Masih bisa'
			else:
				return Response({'status':'udah expired'}, status = status.HTTP_401_UNAUTHORIZED)
			
			if vendor.username == 'Absensee':
				if license.attendance == '2':
					state = 'IsAdmin'
				elif license.attendance == '1':
					state = 'IsUser'
				else:
					state = 'IsNothing'

			elif vendor.username == 'Billing':
				if license.billing == '2':
					state = 'IsAdmin'
				elif license.billing == '1':
					state = 'IsUser'
				return Response({'status':state}, status = status.HTTP_200_OK)

			elif vendor.username == 'ERP':
				if license.attendance == '2':
					state = 'IsAdmin'
				elif license.attendance == '1':
					state = 'IsUser'
				else:
					return Response({'status':'Unauthorized'}, status = status.HTTP_401_UNAUTHORIZED)

				token = ERP_token_generator()		 

				# payload = {
				# 'id_user':user.id,
				# 'name':user.full_name,
				# 'state':state,
				# 'token':token
				# }

				if settings.FLAG == 0:
					url = 'http://dev-erp-api.mindzzle.com/login/savetoken/'
				elif settings.FLAG == 1:
					url = 'https://erp-api.mindzzle.com/login/savetoken/'
				elif settings.FLAG == 3:
					url = 'http://127.0.0.1:8088/login/savetoken/'

				payload_erp = {
				'id_user':user.id,
				'username':user.full_name,
				'token':token
				}

				Req = requests.post(url + str(user.id), data = payload_erp)
				Res = Req.json()

				return Response(Res, status = status.HTTP_200_OK)
					
			elif vendor.username == 'payroll':					
				if license.payroll == '2':
					state = 'IsAdmin'
				elif license.payroll == '1':
					state = 'IsUser'
				else:
					state = 'IsNothing'

				payload = {
				'token':user.token,
				'status': state,
				'id_comp': comp.id,
				'masa':masa
				}
				act = "this user accessing Payroll app"
				read_log(request, user, act)
				return Response(payload, status = status.HTTP_200_OK)
			else:
				return Response({'status':'Vendor Belum Terintegrasi Dengan Mindzzle'})					
			#---------------------------------------------------------

			# user = Register.objects.get(email = email)
			multiple_login = MultipleLogin.objects.get(id_user = user.id)
			#-------------------only single phone-------------------
			if multiple_login.token_phone != 'xxx':
				return Response({'status':'You Have Login In Multiple Phone Devices, Please Logout first'},status = status.HTTP_401_UNAUTHORIZED)
			#-------------------------------------------------------
			attempt = user.attempt
			salt = user.full_name
			salt_password = ''.join(str(ord(c)) for c in salt)
			thepassword = password + salt_password

			if (check_password(thepassword, user.password)):			
				token = make_password(str(time.time()))
				payload = {
				'id_user':user.id,
				'token_web':user.token,
				'token_phone':token
				}
				serializer = MultipleSerializer(multiple_login, data = payload)
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
					act = "this user accessing "+vendor.username+" app"
					read_log(request, user, act)
					multidevices_email(request, user)
					return Response(payload, status = status.HTTP_200_OK)
				return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
				#---------------------------------------------------
				
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
			
		elif request.method == 'GET':
			token = request.META.get('HTTP_AUTHORIZATION')
			user = Register.objects.get(token = token)
			if user.id == 0:
				migrates = Register.objects.all().values_list('id', 'token').filter(verfied = 1)
				result = []
				for id_user, token in migrates:
					payload = {
					'id_user':id_user,
					'token_web':token,
					'token_phone':'xxx'
					}
					serializer = MultipleSerializer(data = payload)
					if serializer.is_valid():
						serializer.save()
						result.append(serializer.data)
				return Response({'status':result}, status = status.HTTP_201_CREATED)
			return Response({'status':'You Do Not Have Super Admin Credentials'}, status = status.HTTP_401_UNAUTHORIZED)
		elif request.method == 'PUT':
			token_vendor = 	request.META.get('HTTP_AUTHORIZATION')
			token_user = request.data['token_user']
			vendor = Vendor_api.objects.get(token = token_vendor)
			user = Register.objects.get(token = token_user)
			multiple_login = MultipleLogin.objects.get(id_user = user.id)
			payload = {
			'id_user':user.id,
			'token_web':user.token,
			'token_phone':'xxx'}
			serializer = MultipleSerializer(multiple_login, data = payload)
			if serializer.is_valid():
				serializer.save()
				act = "this user Logout "+vendor.username+" app"
				read_log(request, user, act)
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
	except MultipleLogin.DoesNotExist:
		return Response({'status':'User is not Registered in multiple devices.'}, status = status.HTTP_401_UNAUTHORIZED)


#---------------------------------------ATTENDANCE API------------------------------------------------------------------------------------
@api_view(['POST', 'PUT'])
def api_login_absensee(request):	
	try:
		token_vendor = request.META.get('HTTP_AUTHORIZATION')
		if token_vendor == 'xxx':
			return Response({
				'status': 'Vendor Token, is Unauthorized.'}, status=status.HTTP_401_UNAUTHORIZED)

		# check method
		if request.method == 'POST':
			email = request.data['email']
			password = request.data['password']

			user = Register.objects.get(email=email)
			full_name = user.full_name
			salt_password = ''.join(str(ord(c)) for c in full_name)
			_password = password + salt_password

			# check login
			if check_password(_password, user.password):
				token = make_password(str(time.time()))

				multiple_login = MultipleLogin.objects.get(id_user=user.id)

				# check condition if token phone already login at another phone
				if multiple_login.token_phone != "xxx":
					payloads = {
						'id_user': user.id,
						'token_web': user.token,
						'token_phone': "xxx"
					}

					_del_token_phone = MultipleSerializer(multiple_login, data=payloads)
					if _del_token_phone.is_valid():
						_del_token_phone.save()

				payload = {
					'id_user': user.id,
					'token_web': user.token,
					'token_phone': token
				}

				serializer = MultipleSerializer(multiple_login, data=payload)

				if serializer.is_valid():
					serializer.save()
					profil = {
						'id': user.id,
						'name': user.full_name,
						'photo': user.url_photo
					}

					payloads = {
						'api_status': 1,
						'api_message': 'success',
						'profile': profil,
					}

					return Response(payloads, status=status.HTTP_201_CREATED)

				else:
					return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
			else:
				attempt_login(request, email)
				response = {'status': 'Wrong Username / Password'}
				return Response(response, status=status.HTTP_400_BAD_REQUEST)
		elif request.method == 'PUT':
			token_user = request.data['token_user']
			vendor = Vendor_api.objects.get(token=token_vendor)
			multiple_login = MultipleLogin.objects.get(token_phone=token_user)
			user = Register.objects.get(id=multiple_login.id_user)
			payload = {
				'id_user': user.id,
				'token_web': user.token,
				'token_phone': 'xxx'}
			serializer = MultipleSerializer(multiple_login, data=payload)
			if serializer.is_valid():
				serializer.save()
				return Response({'status': 'User Has Logout'}, status=status.HTTP_200_OK)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		# if request.method == 'POST':
		# 	token_vendor = request.META.get('HTTP_AUTHORIZATION')
		# 	if token_vendor == 'xxx':
		# 		return Response({'status':'Vendor Token, is Unauthorized.'}, status = status.HTTP_401_UNAUTHORIZED)
		# 	vendor = Vendor_api.objects.get(token = token_vendor)
		#
		# 	email = request.data['email']
		# 	password = request.data['password']
		# 	user = Register.objects.get(email = email)
		# 	attempt = user.attempt
		# 	salt = user.full_name
		# 	salt_password = ''.join(str(ord(c)) for c in salt)
		# 	thepassword = password + salt_password
		#
		# 	if (check_password(thepassword, user.password)):
		# 		token = make_password(str(time.time()))
		# 		#------------------------multiple login--------------------------------
		# 		payload = {
		# 		'id_user':user.id,
		# 		'token_web':user.token,
		# 		'token_phone':token
		# 		}
		# 		multiple_login = MultipleLogin.objects.get(id_user = user.id)
		# 		#-------------------only single phone-------------------
		# 		# if multiple_login.token_phone != 'xxx':
		# 		# 	return Response({'status':'You Have Login In Multiple Phone Devices, Please Logout first'},status = status.HTTP_401_UNAUTHORIZED)
		# 		#-------------------------------------------------------
		# 		serializer = MultipleSerializer(multiple_login, data = payload)
		# 		#----------------------------------------------------------------------
		# 		if serializer.is_valid():
		# 			serializer.save()
		# 			companies = Joincompany.objects.all().values_list('id_company', flat = True).filter(id_user = user.id, status = '2')
		# 			comp = []
		#
		# 			for company in companies:
		# 				beacon = Business.objects.get(id = company)
		# 				hirarki = Hierarchy.objects.get(id_company  = company, id_user = user.id)
		# 				try:
		# 					license = LicenseComp.objects.get(id_hierarchy = hirarki.id, status = '1')
		# 					sekarang = datetime.datetime.now().date()
		# 					if datetime.datetime.strptime(str(license.expr_date), '%Y-%m-%d').date() >= sekarang:
		# 						masa = 'Masih bisa'
		# 					else:
		# 						return Response({'status':'udah expired'}, status = status.HTTP_401_UNAUTHORIZED)
		#
		# 					if license.attendance == '2':
		# 						level = 'IsAdmin'
		# 					elif license.attendance == '3':
		# 						level = 'IsSuperAdmin'
		# 					elif license.attendance == '1':
		# 						level = 'IsUser'
		# 					else:
		# 						level = 'User / Company Belum Mengaktifkan Fitur Ini'
		# 					payload = {
		# 					'token_user': token,
		# 					'image': beacon.logo_path,
		# 					'comp_id': beacon.id,
		# 					'comp_name': beacon.company_name,
		# 					'comp_logo':beacon.logo_path,
		# 					'level' : level
		# 					}
		# 					comp.append(payload)
		# 				except LicenseComp.DoesNotExist:
		# 					pass
		#
		# 			profil = {
		# 			'id':user.id,
		# 			'name':user.full_name,
		# 			'photo':user.url_photo
		# 			}
		#
		# 			payloads = {
		# 				'api_status':1,
		# 				'api_message':'success',
		# 				'profile': profil,
		# 				'companies':comp
		# 			}
		# 			multidevices_email(request, user, serializer.data['token_phone'])
		# 			return Response(payloads, status = status.HTTP_201_CREATED)
		#
		# 		else:
		# 			return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)
		# 	else:
		# 		if (attempt == 0):
		# 			attempt_login(request, email)
		# 			response = {'status' : 'Wrong Username / Password'}
		# 			return Response(response, status=status.HTTP_400_BAD_REQUEST)
		# 		elif(attempt % 5 == 0):
		# 			forget_attempt(request, email)
		# 			return Response(forget_attempt, status=status.HTTP_401_UNAUTHORIZED)
		# 		else:
		# 			attempt_login(request, email)
		# 			response = {'status' : 'Wrong Username / Password'}
		# 			return Response(response, status=status.HTTP_400_BAD_REQUEST)
		# 	# return Response({'status':'Invalid Username or Password'}, status = status.HTTP_401_UNAUTHORIZED)
		# elif request.method == 'PUT':
		# 	token_vendor = 	request.META.get('HTTP_AUTHORIZATION')
		# 	token_user = request.data['token_user']
		# 	vendor = Vendor_api.objects.get(token = token_vendor)
		# 	# user = Register.objects.get(token = token_user)
		# 	multiple_login = MultipleLogin.objects.get(token_phone = token_user)
		# 	user = Register.objects.get(id = multiple_login.id_user)
		# 	payload = {
		# 	'id_user':user.id,
		# 	'token_web':user.token,
		# 	'token_phone':'xxx'}
		# 	serializer = MultipleSerializer(multiple_login, data = payload)
		# 	if serializer.is_valid():
		# 		serializer.save()
		# 		return Response({'status':'User Has Logout'}, status = status.HTTP_200_OK)
		# 	return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

	except Vendor_api.DoesNotExist:
		return Response({'status': 'Vendor Token, is Unauthorized.'}, status=status.HTTP_401_UNAUTHORIZED)
	except Register.DoesNotExist:
		return Response({'status': 'Wrong Username / Password'}, status=status.HTTP_401_UNAUTHORIZED)
	except Joincompany.DoesNotExist:
		return Response({'status': 'User did not have any company'}, status=status.HTTP_202_ACCEPTED)
	except Business.DoesNotExist:
		return Response({'status': 'The Company Does Not Exist'}, status=status.HTTP_202_ACCEPTED)
	# except LicenseComp.DoesNotExist:
	# 	return Response({'stat':hirarki.id,'status':'User is not Registered in License company.'}, status = status.HTTP_401_UNAUTHORIZED)
	# except Hierarchy.DoesNotExist:
	# 	return Response({'status':'Hierarchy does not exist.'}, status = status.HTTP_401_UNAUTHORIZED)
	except MultipleLogin.DoesNotExist:
		return Response({'status': 'User is not Registered in multiple devices.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def logout_by_email(request):
	if request.method == 'GET':
		if settings.FLAG == 0:
			url = 'http://dev-user-api.mindzzle.com/vendor/api/api_login_absensee/'
		elif settings.FLAG == 1:
			url = 'https://x-user-api.mindzzle.com/vendor/api/api_login_absensee/'
		elif settings.FLAG == 2:
			url = 'http://staging-user-api.mindzzle.com/vendor/api/api_login_absensee/'
		elif settings.FLAG == 3:
			url = 'http://127.0.0.1:8000/vendor/api/api_login_absensee/'

		header = {'Authorization' : 'pbkdf2_sha256$120000$I2BCKb0Nflgy$96qeihph6v7Ibpy4st7u5WAFBIRxOUKxHB28r8NlM5U='}
		token = request.query_params.get('token')
		payload = {'token_user':token}
		req = requests.put(url, headers=header, data=payload)
		res = req.json()
		return Response(res, status=status.HTTP_200_OK)

@api_view(['GET'])
def migrate_multiuser_company(request, pk):
	try:
		result = []
		token = request.META.get('HTTP_AUTHORIZATION')
		suser = Register.objects.get(token = token)
		if suser.id == 0:
			join = Joincompany.objects.all().values_list('id_user', flat = True).filter(id_company = pk, status = '2')
			
			for id_user in join:
				user = Register.objects.get(id = id_user)
				try:
					hirarki = Hierarchy.objects.get(id_user = id_user, id_company = pk)
					license = LicenseComp.objects.get(id_hierarchy = hirarki.id)
					if license.attendance == '0':
						payload = {
						'id_user':user.id,
						'name':'Your Attendance Is Not Active',
						'photo':'Your Attendance Is Not Active'
						}
						result.append(payload)
						pass
						# return Response({'status':'Your Attendance is not Active'}, status = status.HTTP_401_UNAUTHORIZED)
					payload = {
					'id_user':user.id,
					'name':user.full_name,
					'photo':user.url_photo
					}
					serializer = MultipleSerializer(data = payload)
					if serializer.is_valid():
						try:
							serializer.save()
							rest = serializer.data
							result.append(rest)
						except Exception:
							pass
							rest = serializer.errors
							result.append(rest)	
				except Hierarchy.DoesNotExist:
					payload = {
						'id_user':user.id,
						'name': 'Your id is not attached in Company Hierarcy',
						'photo':'Your id is not attached in Company Hierarcy'
						}
					result.append(payload)
					pass
				except LicenseComp.DoesNotExist:
					payload = {
						'id_user':user.id,
						'name':'Your id is not attached in License Company ',
						'photo':'Your id is not attached in License Company'
						}
					result.append(payload)
					pass
					# return Response({'status':str(user.id)+' Hierarchy Does Not Exist'}, status = status.HTTP_401_UNAUTHORIZED)
			return Response({'status':result}, status = status.HTTP_201_CREATED)
		else:
			return Response({'status':'You Are Not Super User'}, status = status.HTTP_401_UNAUTHORIZED)
	except Register.DoesNotExist:
		return Response({'status':'Token is Invalid'}, status = status.HTTP_401_UNAUTHORIZED)
	# except LicenseComp.DoesNotExist:
	# 	return Response({'status':'Your License is not Active'}, status = status.HTTP_401_UNAUTHORIZED)
	# except Hierarchy.DoesNotExist:
	# 	return Response({'status':'Hierarchy Does Not Exist'}, status = status.HTTP_401_UNAUTHORIZED)
	except Joincompany.DoesNotExist:
		return Response({'status':'Your Attendance is not Active'}, status = status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def check_token(request):
	if request.method == 'GET':
		try:
			token_ven = request.META.get('HTTP_AUTHORIZATION')
			tokenhp = request.data['token_user']
			beaconhp = MultipleLogin.objects.get(token_phone = tokenhp)
			token = beaconhp.token_web
			beacon_vendor = Vendor_api.objects.get(token = token_ven)
			beacon = Register.objects.get(token = token)
			return Response({'status':'Okay','token':beacon.token,'id':beacon.id},status = status.HTTP_200_OK)
		except Vendor_api.DoesNotExist:
			return Response({'status':'Vendor Token, is Unauthorized.'}, status = status.HTTP_401_UNAUTHORIZED)
		except Register.DoesNotExist:
			return Response({'status':'User Token, is Unauthorized.'}, status = status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def check_admin_attendace(request):
	if request.method == 'POST':
		token = request.META.get('HTTP_AUTHORIZATION')
		try:
			vendor = Vendor_api.objects.get(token = token)
			tokenhp = request.data['token_user']
			# beacon = MultipleLogin.objects.get(token_web = tokenhp)
			# token_user = beacon.token_web
			id_comp = request.data['id_company']
			user = Register.objects.get(token = tokenhp)
			company = Business.objects.get(id = id_comp)
			hirarki = Hierarchy.objects.get(id_user = user.id, id_company = company.id)
			license_comp = LicenseComp.objects.get(id_comp = id_comp, status = '1', id_hierarchy = hirarki.id)
			if license_comp.attendance == '1':
				return Response({'status':'User is not Admin'}, status = status.HTTP_401_UNAUTHORIZED)
			elif license_comp.attendance == '2':
				persona = {
				'id':user.id,
				'name':user.full_name
				}

				bisnis = {
				'id' : company.id,
				'name':company.company_name
				}
				payload = {
				'status':'IsAdmin',
				'User':persona,
				'Company':bisnis
				}
				return Response(payload, status = status.HTTP_200_OK)
			else:
				return Response({'status':'User is unauthorized at all in this page'}, status = status.HTTP_401_UNAUTHORIZED)
		except Vendor_api.DoesNotExist:
			return Response({'status':'Vendor Token, is Unauthorized.'}, status = status.HTTP_401_UNAUTHORIZED)
		except Register.DoesNotExist:
			return Response({'status':'User token is Invalid.'}, status = status.HTTP_401_UNAUTHORIZED)
		except Business.DoesNotExist:
			return Response({'status':'The Company Does Not Exist'}, status = status.HTTP_202_ACCEPTED)
		except LicenseComp.DoesNotExist:
			return Response({'stat':hirarki.id,'status':'User is not Registered in License company.'}, status = status.HTTP_401_UNAUTHORIZED)
		except Hierarchy.DoesNotExist:
			return Response({'status':'Hierarchy does not exist.'}, status = status.HTTP_401_UNAUTHORIZED)
		except MultipleLogin.DoesNotExist:
			return Response({'stat':hirarki.id,'status':'Multiple Login does not exist.'}, status = status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def cloning_data_reprime(request):
	if request.method == 'GET':
		try:
			token = request.META.get('HTTP_AUTHORIZATION')
			vendor = Vendor_api.objects.get(token = token)
			id_company = request.data['id_company']
			company = Business.objects.get(id = id_company)
			hirarki = Hierarchy.objects.all().values_list('id', flat = True).filter(id_company = company.id)
			result = []
			for id_hirar in hirarki:
				hier = Hierarchy.objects.get(id = id_hirar)
				if hier.id_user == 0:
					pass
				else:
					try:
						user = Register.objects.get(id  = hier.id_user)
						license = LicenseComp.objects.get(id_hierarchy = hier.id)				
						if license.attendance == '2':
							level = 'IsAdmin'
						elif license.attendance == '1':
							level = 'IsUser'
						else:
							level = 'User / Company Belum Mengaktifkan Fitur Ini'
						payload = {
						'id' : user.id,
						'fullname' : user.full_name,
						'photo' : user.url_photo,
						'email':user.email,
						'level':level
						}
						result.append(payload)
					except LicenseComp.DoesNotExist:
						# payload = {'id':user.id}
						# result.append(payload)
						pass
                #----------------asdasd-------------
# 				result.append(license.id)
# 			return Response({'status':result}, status = status.HTTP_200_OK)
			payloads = {
			'company_id': company.id,
			'company_name':company.company_name,
			'logo':company.logo_path,
			'employees':result
			}
			return Response(payloads, status = status.HTTP_200_OK)
		except Vendor_api.DoesNotExist:
			return Response({'status':'Vendor Token, is Unauthorized.'}, status = status.HTTP_401_UNAUTHORIZED)
		except Business.DoesNotExist:
			return Response({'status':'The Company Does Not Exist'}, status = status.HTTP_202_ACCEPTED)
		except Hierarchy.DoesNotExist:
			return Response({'status':'Hierarchy does not exist.'}, status = status.HTTP_401_UNAUTHORIZED)
		# except LicenseComp.DoesNotExist:
		# 	return Response({'status':'License Company does not exist.'}, status = status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def timesheets_absensee(request):
	if settings.FLAG == 0:
		url = 'http://dev-attandance.mindzzle.com/api/timesheets'
	elif settings.FLAG == 1:
		url = 'https://attandance.mindzzle.com/api/timesheets'

	Req = requests.get(url)
	Res = Req.json()
	return Response(Res, status = status.HTTP_200_OK)

@api_view(['GET'])
def api_find_company_absensee(request):
	try:
		token_vendor = request.META.get('HTTP_AUTHORIZATION')
		vendor = Vendor_api.objects.get(token = token_vendor)
		tokenhp = request.data['token_user']
		beacon = MultipleLogin.objects.get(token_phone = tokenhp)
		token = beacon.token_web
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

#-------------------------------------DOMOO API-------------------------------------------------------------------------------------------
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
			return Response(seralizer.data)
		return Response(seralizer.errors)
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
				return Response({'status':'Silahkan verifikasi akun Domoo anda', 'Balance':cust['balance'],'Benefit':cust['benefit']})
			elif cust['status'] == '1':
				return Response({'status':'1','Balance':cust['balance'],'Benefit':cust['benefit']})
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
				return Response(seralizer.data)
			return Response(seralizer.errors)
		except Domoo.DoesNotExist:
			return Response({'status': 'Not Domoo User'})
		return Response(resp)
	except Exception:
		resp = Res['message']
		return Response(resp)

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
		return Response(resp)
	except Exception:
		resp = Res['message']
		return Response(resp)

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
			return Response(resp)
		except Exception:
			resp = Res['message']
			return Response(resp)

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

#---------------------------------------------SUper ADmin API -----------------------------------------------------
@api_view(['GET'])
def email_forget_blast(request):
	# awal = request.data['awal']
	# akhir = request.data['akhir']
	emails = request.FILES['list_email']
	df = pd.read_excel(emails)
	email = df['email']

	# emails = [
	# 'ryanlande.bko@jeera.id',
	# 'trisudarmanto309@gmail.com',
	# 'arfshah94@gmail.com',
	# 'Rizkyramadhan0130@gmail.com',
	# 'rezarahmana2643@gmail.com',
	# 'daridermawan@gmail.com',
	# 'meigiwibisono.om@jeera.id',
	# 'elita.finance@jeera.id',
	# 'rifkymoh1204@gmail.com',
	# 'errygani@gmail.com',
	# 'ilham.fajar25789@gmail.com',
	# 'dennyfebri5@gmail.com',
	# 'irtob0161@gmail.com',
	# 'imrideo@gmail.com',
	# 'ferdiardiansyah.logistic@jeera.id',
	# 'nuaric27@gmail.com',
	# 'bonang.pardede@gmail.com',
	# 'akbarkhusaini0512@gmail.com',
	# 'michaelchow9900@gmail.com',
	# 'bobhasan110184@gmail.com',
	# 'farezagazzi@gmail.com',
	# '0pankbregaz21@gmail.com',
	# 'ahmadumarzaman@gmail.om',
	# 'mohamadrizal201@gmail.com',
	# 'Bmtj2286@gmail.com',
	# 'Ediujang12@yahoo.com',
	# 'alinvnd04@gmail.com',
	# 'raflesalviner@gmail.com',
	# 'iimibrahim9322@gmail.com',
	# 'irtob0161@gmail.com',
	# 'marcoarnold.om@jeera.id',
	# 'ibrahimjeratb2019@gmail.com',
	# 'jerianjeeratb2019@gmail.com',
	# 'alinvnd04@gmail.com',
	# 'arfanimoushowwir@gmail.com',
	# 'kevintobing03@gmail.com',
	# 'ferdiardiansyah.logistic@jeera.id',
	# 'michaelchow9900@gmail.com',
	# 'nuaric27@gmail.com',
	# 'tigaraksa.finance@jeera.id',
	# 'jarnuhi.logistic@jeera.id',
	# 'fendykiswantoro69@yahoo.com',
	# 'andrimahonk@gmail.com',
	# 'mikhael.jimmy1979@gmail.com',
	# 'opangsentiong@gmail.com',
	# 'edgartobing4848@gmail.com',
	# 'enitagaja@gmail.com',
	# 'friskopdsitompul@gmail.com',
	# 'reydelaki698@gmail.com',
	# 'yandiimaulana@gmail.com',
	# 'ramadoniasnawi14@gmail.com',
	# 'andicaniago68@gmail.com',
	# 'iyanjeera@gmail.com',
	# 'cecep96@gmail.com',
	# 'yossuseno@gmail.com',
	# 'egisetiawan2312@gmail.com',
	# 'adam.alan233@gmail.com',
	# 'lioapri75@gmail.com',
	# 'praztyo161016@gmail.com',
	# 'ashterendik22@gmail.com',
	# 'altaroli.deni90@gmail.com',
	# 'chandrapalembang28@gmail.com',
	# 'rizalblaaze8946@gmail.com',
	# 'fajrimartienjeera@gmail.com',
	# 'huntertobing@gmail.com',
	# 'erikdwiprasetiyo02@gmail.com',
	# 'kevingamas10@gmail.com',
	# 'dhandyfurna1995@gmail.com',
	# 'dennyuyee656@gmail.com',
	# 'maded5731@gmail.com',
	# 'lkthap027@gmail.com',
	# 'choirudin.finance@jeera.id',
	# 'biyansofian23@gmail.com',
	# 'hendrasinabutar.logistic@jeera.id',
	# 'robirosadi1612@gmail.com',
	# 'pratama13420@gmail.com',
	# 'akbarwidodo1791@gmail.com',
	# 'sultanmahdawi@gmail.com',
	# 'rezaapriandi91@gmail.com',
	# 'rahmadhadil662@gmail.com',
	# 'Sfadlurrahman25@gmail.com',
	# 'daniel93mihado@gmail.com',
	# 'apriadisitumorang123@gmail.com',
	# 'rijalamsari@741gmail.com',
	# 'agusdaniel50477@gmail.com',
	# 'marlogustaf27@gmail.com',
	# 'muhammadhaswar2808@gmail.com',
	# 'hakimjr106@gmail.com',
	# 'nurfadliarfah96@gmail.com',
	# 'muradalbarack@gmail.com',
	# 'aan3346036@gmail.com',
	# 'armanto.jeera@gmail.com',
	# 'vivi170198@gmail.com',
	# 'puranto56@gmail.com',
	# 'ncitraa25@gmail.com',
	# 'agungpikachu983@gmail.com',
	# 'abriansyah.arif0501@gmail.com',
	# 'anggun.shelly0901@gmail.com',
	# 'yuliojigwhen09@gmail.com',
	# 'elvinrizky3@gmail.com',
	# 'diantriangga69@gmail.com',
	# 'khalidin02@yahoo.com',
	# 'dearizky97@yahoo.co.id',
	# 'barnesahza@gmail.com',
	# 'Imraniponk5@gmail.com',
	# 'marshelsihotangj@gmail.com',
	# 'suhartantobagus.logistic.@jeera.id',
	# 'dingblen3@gmail.com',
	# 'Ifangaluhpesek@gmail.com',
	# 'hermawansurya2706@gmail.com',
	# 'febrialfano23@gmail.com',
	# 'erwin.prc98@gmail.com',
	# 'suriadi.bambang@gmail.com',
	# 'muhammadrijal429@gmail.com',
	# 'zackharefa@gmail.com',
	# 'tora.manurung@yahoo.com',
	# 'jordantobing23@gmail.com',
	# 'arga65656@gmail.com',
	# 'boynanta21@gmail.com',
	# 'bernart1411@gmail.com',
	# 'chandrasamosir02@gmail.com',
	# 'fadliskrn@yahoo.com',
	# 'tengkurahmadani2017@gmail.com',
	# 'bprasetyo109@gmail.com',
	# 'rome724@gmail.com',
	# 'andidiego63@gmail.com',
	# 'andrisupriyadi170@gmail.com',
	# 'jollypangkey30@gmail.com',
	# 'hrudi9524@gmail.com',
	# 'boymanik04@gmail.com',
	# 'herberth.aja@gmail.com',
	# 'malang.finance@jeera.id',
	# 'faiz.jeera@gmai.com',
	# 'deniwahyu19@gmail.com',
	# 'galuh8612@gmail.com',
	# 'izzatmaliki23@gmail.com',
	# 'alizen2898@gmail.com',
	# 'bondanherlambang2000@gmail.com',
	# 'ariyanto0901@gmail.com',
	# 'harijo0883@gmail.com',
	# 'muhsahrul0399@gmail.com',
	# 'nurkamal230394@gmail.com',
	# 'reski.mumtahana05@gmail.com',
	# 'nilaanggraeni1983@gmail.com',
	# 'Contoh@mailinator.com'
	# ]
	# token = request.META.get('HTTP_AUTHORIZATION')
	# admin = Register.objects.get(token = token)
	respon = []
	# for eml in range(0,len(email)):
	# 	email = email[eml]
	for email in emails:
		try:
			user = Register.objects.get(email = email)
			key = 'Jeera1234'+user.salt_password
			token_forget = 'usethistokenforforgetyourpassword'
			if check_password(key,user.password):
				if user.banned_type != '0':
					url = 'https://user-api.mindzzle.com/registrations/api/forget/'
					payload = {
					'email': user.email
					}
					Req = requests.post(url, data = payload)
					Res = Req.json()
					respon.append(payload)
				else:
					serializer = forgetblastSerializer(user,  data = {'banned_type':'1','verified':1})
					if serializer.is_valid():
						serializer.save()
						respon.append(str(user.id)+'. '+email + ' : Get Banned')
					else:
						respon.append(serializer.errors)
						pass
			elif check_password(token_forget, user.password):
				if user.banned_type != '0':
					respon.append(str(user.id)+'. '+email + ' : Has Forget their password') 
				else:
					serializer = forgetblastSerializer(user,  data = {'banned_type':'1','verified':1})
					if serializer.is_valid():
						serializer.save()
						respon.append(str(user.id)+'. '+email + ' : Has Forget their password And Get Banned')
					else:
						respon.append(serializer.errors)
				pass
			else:
				if user.banned_type != '0':
					respon.append(str(user.id)+'. '+email + ' : Password Has Changed')
				else:
					serializer = forgetblastSerializer(user,  data = {'banned_type':'1','verified':1})
					if serializer.is_valid():
						serializer.save()
						respon.append(str(user.id)+'. '+email + ' : Password Has Changed But Get banned')
					else:
						respon.append(serializer.errors)
				pass
		except Register.DoesNotExist:
			respon.append(email + ' : does not exist')
			pass
			# return Response({'status':'User Not Found'}, status = status.HTTP_404_NOT_FOUND)
	return Response(respon, status = status.HTTP_200_OK)
		# else:
		# 	return Response({'status':'Unauthorized'}, status = status.HTTP_401_UNAUTHORIZED)
	

# @api_view(['GET'])
# def email_blast(request):
# 	awal = request.data['awal']
# 	akhir  = request.data['akhir']
# 	respon = []
# 	try:
# 		for id_user in range(int(awal), int(akhir)):
# 			user = Register.objects.get(id = id_user)

@api_view(['POST'])
def send_blast(request):
  if request.method == 'POST':
    awal = request.data['awal']
    akhir  = request.data['akhir']
    result = []
    try:
        for id_user in range(int(awal), int(akhir)):
    # #--------------DATA---------------------	   
            user = Register.objects.get(id = id_user)
            recipient = user.email
            msg = EmailMessage(
              'Info Mobile Apps Mindzzle',
              'Silahkan Untuk Download aplikasi Mindzzle dengan link dibawah ini \n Android : https://play.google.com/store/apps/details?id=com.reprime.mindzzle.attendance \n IOS : https://apps.apple.com/id/app/mindzzle-attendance/id1463349473',
              'admin@mindzzle.com',
              [recipient],      
              )
            # try:
            msg.send()
            sre ={'status':str(user.email)+' Berhasil Dikirim'}
            result.append(sre)
            # except Exception:
            #     sre ={'status':str(user.email)+' Gagal Dikirim'}
            #     result.append(sre)
    except Register.DoesNotExist:
      	pass        
    return Response(result)

@api_view(['GET'])
def download_data(request):
	items = MultipleLogin.objects.all()

	response  = HttpResponse(content_type = 'text/csv')
	response['Content-Disposition'] = 'attachment;filename = "multiplelogin.csv"'

	writer = csv.writer(response, delimiter = ',')
	writer.writerow(['id_user','token_web','token_phone'])

	for obj in items:
		writer.writerow([obj.id_user, obj.token_web, obj.token_phone])

	return response

@api_view(['GET'])
def employee_cred(request):
	id_comp = request.data['id_comp']
	result = []
	try:
		beacon = Hierarchy.objects.all().values_list('id_user', 'division').filter(id_company = id_comp)
		comp = Business.objects.get(id = id_comp)		
		for userId, div in beacon:
			try:
				user = Register.objects.get(id = userId).full_name
				# dalaman = {'division':div, 'name':user}
				if userId == 0:
					pass
				else:
					hasil = {'id_user':userId,'division':div, 'name':user, 'comp_name':comp.company_name}
					result.append(hasil)
			except Register.DoesNotExist:
				resp = 'user '+userId +' does not exist'
				result.append(resp)
				pass
		return Response(result)
	except Business.DoesNotExist:
		return Response({'status':'id company does not match !'})
	except Hierarchy.DoesNotExist:
		return Response({'status':'Hierarchy Company does not exist !'})
	
