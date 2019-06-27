from rest_framework import serializers
from .models import GoalPin

class GoalPinSerializer(serializers.ModelSerializer):
	class Meta:
		model = GoalPin
		fields = '__all__'