from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import PersonalChat, GroupChat, PersonelGroupChat
from .serializers import PersonalChatSerializer, GroupChatSerializer, PersonelSerializer
from registrations.models import Register

@api_view(['GET','POST'])
def get_post_pchat(request,pk):
    try:
        token = request.META.get('HTTP_AUTHORIZATION')
        user = Register.objects.get(token = token)
        if request.method == 'GET':
            try:               
                beacon = PersonalChat.objects.all().values_list('message', flat =True).filter(sender = user.id ,recipient = pk)
                serializer = PersonalChatSerializer(beacon, many = True)
                return Response(serializer.data, status = status.HTTP_201_CREATED)            
            except PersonalChat.DoesNotExist:
                return Response({'status':'No Content'}, status = status.HTTP_204_NO_CONTENT)
        elif request.method == 'POST':
            payload = {
                'message' : request.data['message'],
                'sender' : user.id,
                'recipient' : pk,
            }
            serializer = PersonalChatSerializer(data = payload)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    except Register.DoesNotExist:
        return Response({'status':'You Must Login First'}, status = status.HTTP_401_UNAUTHORIZED)

@api_view(['GET', 'POST'])
def get_post_gchat(request, pk):
    try:
        token = request.META.get('HTTP_AUTHORIZATION')
        user = Register.objects.get(token = token)
        
        if request.method == 'GET':           
            try:
                beacon = GroupChat.objects.get(id = pk)
                pesan = PersonalChat.objects.all().values_list('sender', 'message').filter(group_id = beacon.id)            
                result = {}
                for sender, message in pesan:
                    result[sender] = message
                return Response(result, status = status.HTTP_201_CREATED)
            except GroupChat.DoesNotExist:
                return Response({'status':'The Gorup Does Not Exist Yet'}, status = status.HTTP_400_BAD_REQUEST)
            except PersonalChat.DoesNotExist:
                return Response({'status':'No One Sent message to this group, you will be the first, maybe'}, status = status.HTTP_204_NO_CONTENT)
        
        elif request.method == 'POST':
            try:
                beacon = GroupChat.objects.get(id = pk)
                payload = {
                    'message' : request.data['message'],
                    'sender' : user.id,                    
                    'group_id' : pk
                }
                serializerchat = PersonalChatSerializer(data = payload)
                if serializerchat.is_valid():
                    serializerchat.save()
                    return Response(serializerchat.data, status = status.HTTP_201_CREATED)
                return Response(serializerchat.errors, status = status.HTTP_400_BAD_REQUEST)

            except GroupChat.DoesNotExist:
                payloads = {
                    'admin': user.id
                }
                serializergroup = GroupChatSerializer(data = payloads)
                if serializergroup.is_valid():
                    serializergroup.save()
                    payload = {
                        'message' : request.data['message'],
                        'sender' : user.id,                    
                        'group_id' : serializergroup.data['id']
                    }
                    serializerchat = PersonalChatSerializer(data = payload)
                    if serializerchat.is_valid():
                        serializerchat.save()
                        return Response(serializerchat.data, status = status.HTTP_201_CREATED)
                    return Response(serializerchat.errors, status = status.HTTP_400_BAD_REQUEST)
                return Response(serializergroup.errors, status = status.HTTP_400_BAD_REQUEST)
    
    except Register.DoesNotExist:
         return Response({'status':'You Must Login First'}, status = status.HTTP_401_UNAUTHORIZED)
    

@api_view(['POST'])
def adding_members(request,pk):
    try:
        token = request.META.get('HTTP_AUTHORIZATION')
        user = Register.objects.get(token = token)
        beacon = GroupChat.objects.get(admin = user.id)
        payload = {
            'personel' : request.data['member_id'],
            'group_id' : beacon.id
        }
        serializer = PersonelSerializer(data = payload)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    except Register.DoesNotExist:
        return Response({'status':'You Must Login First'}, status = status.HTTP_401_UNAUTHORIZED)
    except GroupChat.DoesNotExist:
        return Response({'status':'You Must be the admin group to add new members'}, status = status.HTTP_401_UNAUTHORIZED)

@api_view(['DELETE'])
def delete_message(request,pk):
    try:
        token = request.META.get('HTTP_AUTHORIZATION')
        user = Register.objects.get(token = token)
        message = PersonalChat.objects.get(id = pk, sender = user.id)
        message.delete()
        return Response({'status':'Success'}, status = status.HTTP_204_NO_CONTENT)
    except PersonalChat.DoesNotExist:
        return Response({'status':'Chat Does Not Exist'}, status = status.HTTP_204_NO_CONTENT)
    except Register.DoesNotExist:
        return Response({'status':'You Must Login First'}, status = status.HTTP_401_UNAUTHORIZED)
# def get_put_delete_interview(request, pk):
#     try: 
#         beacon = Interview.objects.get(id = pk)
#         if request.method == 'GET':
#             serializer = InterSerializer(beacon)
#             return Response(serializer.data, status = status.HTTP_201_CREATED)
#         elif request.method == 'DELETE':
#             beacon.delete()
#             return Response({'status':'Success Delete'}, status = status.HTTP_204_NO_CONTENT)
#         elif request.method == 'PUT':
#             serializer = InterSerializer(beacon, data = request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status = status.HTTP_201_CREATED)
#             return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
#     except Interview.DoesNotExist:
#         return Response({'status':'Interview Schedule Does Not Exist'}, status = status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'POST'])
# def get_post_interview(request):
#     if request.method == 'GET':
#         network = Interview.objects.all()
#         serializer = InterSerializer(network, many=True)
#         return Response(serializer.data, status = status.HTTP_201_CREATED)

#     elif request.method == 'POST':
#         serializer = InterSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
