from rest_framework import serializers
from .models import City
from django.contrib.auth.models import User

class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = '__all__'