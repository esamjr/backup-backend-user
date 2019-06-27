from rest_framework import serializers
from .models import ItemCheck

class ItemCheckSerializer(serializers.ModelSerializer):
	class Meta:
		model = ItemCheck
		fields = '__all__'