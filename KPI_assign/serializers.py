from rest_framework import serializers
from .models import kpi_assign


class KpiAssignSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = kpi_assign
        fields = '__all__'