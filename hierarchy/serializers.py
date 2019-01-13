from rest_framework import serializers
from .models import Hierarchy
from django.contrib.auth.models import User

class HierarchySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Hierarchy
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    User = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = User
        fields = '__all__'