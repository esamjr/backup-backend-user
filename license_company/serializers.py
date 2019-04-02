from rest_framework import serializers
from .models import LicenseComp
from django.contrib.auth.models import User

class LicenseCompSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = LicenseComp
        fields = '__all__'
