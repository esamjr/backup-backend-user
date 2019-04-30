from .models import Vendor_api, MultipleLogin
from rest_framework import serializers

class MultipleSerializer(serializers.ModelSerializer):
	class Meta:
		model = MultipleLogin
		fields = '__all__'
		
class VendorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Vendor_api
		fields = '__all__'