from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def upload_file(request):
    name = request.body['name']
    files = request.body['image']
    client = storage.Client('mindzzle-225411')
    bucket = client.get_bucket('mindzzle-data')
    zebraBlob = bucket.get_blob(name)
    zebraBlob.upload_from_filename(filename=files)

    # content_type = 'text/plain'

    # blob.upload_from_string(files, content_type=content_type)

    # url = blob.public_url
    # if isinstance(url, six.binary_type):
    #     url = url.decode('utf-8')

    return Response({'Success'})