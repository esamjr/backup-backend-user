from rest_framework import serializers
from .models import KPIcat

class KPIcatSerializer(serializers.ModelSerializer):
	class Meta:
		model = KPIcat
		fields = '__all__'