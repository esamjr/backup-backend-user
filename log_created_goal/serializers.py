from rest_framework import serializers
from .models import Hierarchy
from registrations.models import Register

class HierarchySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Hierarchy
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Register
        fields = '__all__'