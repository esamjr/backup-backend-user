from rest_framework import serializers
from .models import Register, Domoo
from django.contrib.auth.models import User

class DomoSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Domoo
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Register
        fields = '__all__'

class LoginSerializer(serializers.ModelSerializer):

	class Meta:
		model = Register
		fields = ('email','password', 'token', 'id_type','banned_type', 'attempt',)

class ConfirmSerializer(serializers.ModelSerializer):

	class Meta:
		model = Register
		fields = ('banned_type',)

class ForgetSerializer(serializers.ModelSerializer):

	class Meta:
		model = Register
		fields = ('password','token',)

class SentForgetSerializer(serializers.ModelSerializer):
	class Meta:
		model = Register
		fields = ('token',)

class SearchSerializer(serializers.ModelSerializer):
	class Meta:
		model = Register
		fields = ('full_name','description', 'url_fb','url_linkedin', 'url_instagram' , 'primary_address', 'primary_phone', 'email', 'birth_day','id_country', 'id_regions', 'id_city','url_photo',)

class AttemptSerializer(serializers.ModelSerializer):
	class Meta:
		model = Register
		fields = ('attempt',)

class PassingAttemptSerializer(serializers.ModelSerializer):
	class Meta:
		model = Register
		fields = ('attempt','token',)

class MaxAttemptReachSerializer(serializers.ModelSerializer):
	class Meta:
		model = Register
		fields = ('attempt','token','password',)

class TokenSerializer(serializers.ModelSerializer):
	class Meta:
		model = Register
		fields = ('token',)