from rest_framework import serializers
from .models import AwardBA
from django.contrib.auth.models import User

class AwardBASerializer(serializers.ModelSerializer):

    class Meta:
        model = AwardBA
        fields = '__all__'