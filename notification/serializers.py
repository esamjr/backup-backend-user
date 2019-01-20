from rest_framework import serializers
from .models import Notification
from django.contrib.auth.models import User

class NotificationSerializer(serializers.ModelSerializer):    

    class Meta:
        model = Notification
        fields = '__all__'