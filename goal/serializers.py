from rest_framework import serializers
from .models import Goal2

class GoalSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Goal2
        fields = '__all__'
