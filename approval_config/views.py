from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Approval
from .serializers import ApprovalSerializer
from business_account.models import Business
from registrations.models import Register
from hierarchy.models import Hierarchy
from log_app.views import read_log
from django.shortcuts import get_object_or_404


@api_view(['PUT','GET', 'DELETE'])
def update_lookone_approval(request,pk):
	try:
		if request.method == 'PUT':
			token = request.META.get('HTTP_AUTHORIZATION')
			user = Register.objects.get(token = token)			
			approv = Approval.objects.get(id = pk)
			comp = Business.objects.get(id = approv.id_comp)
			serializers = ApprovalSerializer(approv, data = request.data)
			if serializers.is_valid():
				serializers.save()
				act = 'Edit approval id : '+str(pk)
				read_log(request,user,act)
				return Response(serializers.data, status = status.HTTP_200_OK)
			return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)
		elif request.method == 'GET':
			token = request.META.get('HTTP_AUTHORIZATION')
			user = Register.objects.get(token = token)
			approv = Approval.objects.get(id = pk)
			comp = Business.objects.get(id = approv.id_comp)			
			serializers = ApprovalSerializer(approv)
			return Response(serializers.data, status = status.HTTP_200_OK)
		elif request.method == 'DELETE':
			token = request.META.get('HTTP_AUTHORIZATION')
			user = Register.objects.get(token = token)
			approv = Approval.objects.get(id = pk)
			comp = Business.objects.get(id = approv.id_comp)			
			approv.DELETE()
			act = 'delete approval id : '+str(pk)
			read_log(request,user,act)
			return Response({'status':'Deleted'}, status = status.HTTP_204_NO_CONTENT)		
	except Register.DoesNotExist:
		return Response({'status':'User Did Not Exist'}, status = status.HTTP_401_UNAUTHORIZED)
	except Business.DoesNotExist:
		return Response({'status':'Company Did Not Exist'}, status = status.HTTP_401_UNAUTHORIZED)
	except Approval.DoesNotExist:
		return Response({'status':'Approval Did Not Exist'}, status = status.HTTP_401_UNAUTHORIZED)



@api_view(['POST'])
def migrate_to_approval(request):
	try: # masih kurang parameter, jika satu user manjadi admin di lebih dari 2 company
		if request.method == 'POST':
			token = request.META.get('HTTP_AUTHORIZATION')
			id_comp = request.data['id_comp']
			user = Register.objects.get(token = token)
			comp = Business.objects.get(id_user = user.id, id = id_comp)
			# comps = Business.objects.all().values_list('id', flat = True).filter(id_user = user.id)
			result = []
			# for comp in comps:
			hiers = Hierarchy.objects.all().values_list('id', flat = True).filter(id_company = comp.id)				
			for hie in hiers:
				payload = {
				'id_comp' : comp.id,
				'id_hierarchy' : hie,
				'approval1' : 0,
				'approval2' : 0
				}
				serializers = ApprovalSerializer(data = payload)
				if serializers.is_valid():
					serializers.save()
					act = 'Migrate approval by hierarchy id : '+str(serializers.data['id_hierarchy'])
					read_log(request,user,act)
					result.append(serializers.data)
				else:
					act = 'Failed to migrate approval by hierarchy id : '+str(serializers.data['id_hierarchy'])
					read_log(request,user,act)
					result.append(serializers.errors)
			return Response(result, status = status.HTTP_201_CREATED)

	except Register.DoesNotExist:
		return Response({'status':'User Did Not Exist'}, status = status.HTTP_401_UNAUTHORIZED)
	except Business.DoesNotExist:
		return Response({'status':'Company Did Not Exist'}, status = status.HTTP_401_UNAUTHORIZED)
	except Hierarchy.DoesNotExist:
		return Response({'status':'Hierarchy Did Not Exist'}, status = status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def get_all_approval_by_comp(request, pk):
	try:
		queryset = Approval.objects.filter(id_comp=int(pk))
		serializer = ApprovalSerializer(queryset, many=True)
		return Response(serializer.data)

	except Exception as e:
		raise e.args


# @api_view(['GET'])
# def get_all_approval_by_comp(request,pk):
# 	try:
# 		if request.method == 'GET':
# 			token = request.META.get('HTTP_AUTHORIZATION')
# 			user = Register.objects.get(token = token)
# 			id_comp =pk
# 			result = Approval.objects.all().filter(id_comp = id_comp)
# 			serializer = ApprovalSerializer(result, many = True)
# 			return Response(serializer.data, status = status.HTTP_200_OK)
#
# 	except Register.DoesNotExist:
# 		return Response({'status':'User Did Not Exist'}, status = status.HTTP_401_UNAUTHORIZED)
# 	except Business.DoesNotExist:
# 		return Response({'status':'Company Did Not Exist'}, status = status.HTTP_401_UNAUTHORIZED)
# 	except Hierarchy.DoesNotExist:
# 		return Response({'status':'Hierarchy Did Not Exist'}, status = status.HTTP_401_UNAUTHORIZED)
