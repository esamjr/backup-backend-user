from rest_framework import serializers
from .models import jobdesc
# from django.contrib.auth.models import User

class JobdescSerialiser(serializers.ModelSerializer):
	class Meta:
		model = jobdesc
		fields = '__all__'

# class LoggingSerializer(serializers.ModelSerializer):
#     # name = serializers.ReadOnlyField(source='name.username')

#     class Meta:
#         model = Logging
#         fields = '__all__'
