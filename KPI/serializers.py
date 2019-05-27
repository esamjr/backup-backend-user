from rest_framework import serializers
from .models import Kpi


class KpiSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Kpi
        fields = '__all__'