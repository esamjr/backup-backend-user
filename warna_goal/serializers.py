from rest_framework import serializers
from .models import warna_goal


class WarnaGaolSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = warna_goal
        fields = '__all__'