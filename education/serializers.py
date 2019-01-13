from rest_framework import serializers
from .models import Education
from django.contrib.auth.models import User

class EducationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Education
        fields = '__all__'