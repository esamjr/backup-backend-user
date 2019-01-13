from rest_framework import serializers
from .models import Usertype
from django.contrib.auth.models import User

class UsertypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usertype
        fields = '__all__'
