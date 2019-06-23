from rest_framework import serializers
from .models import CatGoal

class CatGoalSerializer(serializers.ModelSerializer):
	class Meta:
		model = CatGoal
		fields = '__all__'