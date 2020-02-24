from rest_framework import serializers

from .models import LicenseComp


class LicenseCompSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = LicenseComp
        fields = '__all__'
