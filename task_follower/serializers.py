from rest_framework import serializers
from .models import TaskFoll

class TaskFollSerializer(serializers.ModelSerializer):
	class Meta:
		model = TaskFoll
		fields = '__all__'