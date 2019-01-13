from rest_framework import serializers
from .models import Contract
from django.contrib.auth.models import User

class contractSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='name.username')

    class Meta:
        model = Contract
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    Contract = serializers.PrimaryKeyRelatedField(many=True, queryset=Contract.objects.all())

    class Meta:
        model = User
        fields = '__all__'