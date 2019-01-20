from rest_framework import serializers
from .models import Logging
from django.contrib.auth.models import User

class LoggingSerializer(serializers.ModelSerializer):
    # name = serializers.ReadOnlyField(source='name.username')

    class Meta:
        model = Logging
        fields = '__all__'
