from rest_framework import serializers
from .models import Register
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Register
        fields = '__all__'

class LoginSerializer(serializers.ModelSerializer):

	class Meta:
		model = Register
		fields = 'email','password', 'token', 'id_type','banned_type'

class ConfirmSerializer(serializers.ModelSerializer):

	class Meta:
		model = Register
		fields = ('banned_type',)