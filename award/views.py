from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Award as award
from .serializers import AwardSerializer
from .permissions import IsOwnerOrReadOnly

@api_view(['GET', 'DELETE', 'PUT'])
#@permission_classes ((IsAuthenticated, IsOwnerOrReadOnly,))
def get_delete_update_award(request, pk):
    Award = award.objects.get(pk=pk)

    try:       

        if request.method == 'GET':
            serializer = AwardSerializer(Award)
            return Response(serializer.data)

        elif request.method == 'DELETE':
            if(request.user == Award.name_institution):
                Award.delete()
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
            if(request.user == Award.name_institution):
                serializer = AwardSerializer(Award, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                content = {
                    'status': 'UNAUTHORIZED'
                }
                return Response(content, status=status.HTTP_401_UNAUTHORIZED)

    except award.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST'])
#@permission_classes((IsAuthenticated, ))
def get_post_award(request):
    if request.method == 'GET':
        network = award.objects.all()
        serializer = AwardSerializer(network, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AwardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()                
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
#@permission_classes((IsAuthenticated, ))
def get_post_award_user(request,pk):
    try:
        if request.method == 'GET':
            network = award.objects.all().filter(id_user=pk)
            serializer = AwardSerializer(network, many=True)
            return Response(serializer.data)
    except award.DoesNotExist:
        content = {
            'status': 'Not Found'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)


  