from rest_framework import serializers
from .models import Historyhierarchy
from django.contrib.auth.models import User

class HistoryhierarchySerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='name.username')

    class Meta:
        model = Historyhierarchy
        fields = '__all__'
