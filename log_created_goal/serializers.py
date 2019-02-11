from rest_framework import serializers
from .models import log_goal

class LogGoalSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = log_goal
        fields = ('id_company','id_goal','id_hierarchy','id_user','created_at',)

class LogGoalUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = log_goal
        fields = ('update_at',)
