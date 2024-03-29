from rest_framework import serializers
from .models import Jobs, Recruitment

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = '__all__'

class StatusApplySerializer(serializers.ModelSerializer):
	class Meta:
		model = Recruitment
		fields = ('status',)

class RecSerializer(serializers.ModelSerializer):
	class Meta:
		model = Recruitment
		fields = '__all__'