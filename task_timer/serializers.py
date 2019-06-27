from rest_framework import serializers
from .models import TaskTimer

class TaskTimerSerializer(serializers.ModelSerializer):
	class Meta:
		model = TaskTimer
		fields = '__all__'