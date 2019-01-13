from rest_framework import serializers
from .models import Award
from django.contrib.auth.models import User

class AwardSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Award
        fields = '__all__'