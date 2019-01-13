from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Contact as kontak
from .serializers import ContactSerializer
from .permissions import IsOwnerOrReadOnly

@api_view(['GET', 'DELETE', 'PUT'])
#@permission_classes ((IsAuthenticated, IsOwnerOrReadOnly,))
def get_delete_update_contact(request, pk):
    try:
        Contact = kontak.objects.get(pk=pk)
    except Contact.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ContactSerializer(Contact)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if(request.user == Contact):
            contact.delete()
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
        if(request.user == Contact):
            serializer = ContactSerializer(contact, data=request.data)
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
#@permission_classes((IsAuthenticated, ))
def get_post_contact(request):
    if request.method == 'GET':
        network = kontak.objects.all()
        serializer = ContactSerializer(network, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
#@permission_classes((IsAuthenticated, ))
def get_post_contact_user(request,pk):
    if request.method == 'GET':
        network = kontak.objects.all().filter(id_user=pk)
        serializer = ContactSerializer(network, many=True)
        return Response(serializer.data)