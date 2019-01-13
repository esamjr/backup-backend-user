from rest_framework import serializers
from .models import Certification
from django.contrib.auth.models import User

class CertificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Certification
        fields = '__all__'