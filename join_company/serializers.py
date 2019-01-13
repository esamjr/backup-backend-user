from rest_framework import serializers
from .models import Joincompany
from django.contrib.auth.models import User

class JoincompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Joincompany
        fields = '__all__'
