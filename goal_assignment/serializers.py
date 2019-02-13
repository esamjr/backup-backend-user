from rest_framework import serializers
from .models import Goal_assign


class GoalassignSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Goal_assign
        fields = '__all__'