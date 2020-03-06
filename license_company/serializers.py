from rest_framework import serializers

from .models import LicenseComp


class LicenseCompSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = LicenseComp
        fields = '__all__'


class LicenseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LicenseComp
        fields = ['expr_date', 'status', ]


class LicenseUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LicenseComp
        fields = ['attendance', 'payroll', 'status', 'expr_date', ]

