from rest_framework import serializers
from .models import friendlist
from django.contrib.auth.models import User

class FriendlistSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = friendlist
        fields = '__all__'