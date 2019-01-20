from django.shortcuts import render
from google.cloud import storage
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def upload_file(request):
    # filename = request.body['name']
    files = request.FILES['image']
    client = storage.Client('mindzzle-225411')
    bucket = client.get_bucket('mindzzle-data')
    blob = bucket.blob(files)
    # content_type = 'text/plain'

    # blob.upload_from_string(files, content_type=content_type)

    url = blob.public_url
    if isinstance(url, six.binary_type):
        url = url.decode('utf-8')

    return Response(url)