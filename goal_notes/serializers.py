from rest_framework import serializers
from .models import GoalNotes

class GoalNotesSerializer(serializers.ModelSerializer):
	class Meta:
		model = GoalNotes
		fields = '__all__'