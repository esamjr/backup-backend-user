from rest_framework import serializers
from .models import type_goal


class TypegoalSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = type_goal
        fields = '__all__'

