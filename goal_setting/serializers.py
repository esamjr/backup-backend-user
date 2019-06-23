from rest_framework import serializers
from .models import GoalSet

class GoalSetSerializer(serializers.ModelSerializer):
	class Meta:
		model = GoalSet
		fields = '__all__'