from rest_framework import serializers
from .models import Businesstype
from django.contrib.auth.models import User

class BusinesstypeSerializer(serializers.ModelSerializer):
    Businesstype = serializers.ReadOnlyField(source='Businesstype.username')

    class Meta:
        model = Businesstype
        fields = '__all__'
