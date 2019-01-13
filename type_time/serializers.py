from rest_framework import serializers
from .models import Typetime
from django.contrib.auth.models import User

class TypetimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Typetime
        fields = '__all__'