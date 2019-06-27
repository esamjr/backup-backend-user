from rest_framework import serializers
from .models import TemplateCheck

class TemplateCheckSerializer(serializers.ModelSerializer):
	class Meta:
		model = TemplateCheck
		fields = '__all__'