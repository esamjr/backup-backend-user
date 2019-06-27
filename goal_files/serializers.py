from rest_framework import serializers
from .models import GoalFiles

class GoalFilesSerializer(serializers.ModelSerializer):
	class Meta:
		model = GoalFiles
		fields = '__all__'