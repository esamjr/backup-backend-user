from rest_framework import serializers
from .models import Private
from django.contrib.auth.models import User

class PrivateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Private
        fields = '__all__'