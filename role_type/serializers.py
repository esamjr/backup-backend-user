from rest_framework import serializers
from .models import Roletype
from django.contrib.auth.models import User

class RoletypeSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='name.username')

    class Meta:
        model = Roletype
        fields = '__all__'
