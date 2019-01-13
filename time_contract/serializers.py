from rest_framework import serializers
from .models import Timecontract
from django.contrib.auth.models import User

class TimecontractSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='name.username')

    class Meta:
        model = Timecontract
        fields = '__all__'