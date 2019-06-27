from rest_framework import serializers
from .models import TaskComm

class TaskCommSerializer(serializers.ModelSerializer):
	class Meta:
		model = TaskComm
		fields = '__all__'