from rest_framework import serializers
from .models import time_period


class TimeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = time_period
        fields = '__all__'