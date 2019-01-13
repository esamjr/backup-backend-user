from rest_framework import serializers
from .models import Region
from django.contrib.auth.models import User

class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = '__all__'