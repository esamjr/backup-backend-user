from rest_framework import serializers
from .models import task_assign


class TaskAssignSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = task_assign
        fields = '__all__'