from rest_framework import serializers
from .models import CertificationBA
from django.contrib.auth.models import User

class CertificationBASerializer(serializers.ModelSerializer):

    class Meta:
        model = CertificationBA
        fields = '__all__'