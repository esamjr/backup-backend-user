from .models import Vendor_api
from rest_framework import serializers

class VendorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Vendor_api
		fields = '__all__'