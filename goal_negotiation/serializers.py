from rest_framework import serializers
from .models import goal_negotiation


class GoalnegoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = goal_negotiation
        fields = '__all__'

