from rest_framework import serializers
from .models import Experiences
from django.contrib.auth.models import User

class ExperiencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiences
        fields = '__all__'