from rest_framework import serializers
from .models import ActGoal

class ActGoalSerializer(serializers.ModelSerializer):
	class Meta:
		model = ActGoal
		fields = '__all__'