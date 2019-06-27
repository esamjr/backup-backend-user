from rest_framework import serializers
from .models import TaskTag

class TaskTagSerializer(serializers.ModelSerializer):
	class Meta:
		model = TaskTag
		fields = '__all__'