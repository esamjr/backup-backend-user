from rest_framework import serializers
from .models import Jobfair


class JobfairSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Jobfair
        fields = '__all__'
