from rest_framework import serializers
from .models import Level
from django.contrib.auth.models import User

class LevelSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='name.username')

    class Meta:
        model = Level
        fields = '__all__'
