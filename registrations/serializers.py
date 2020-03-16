from rest_framework import serializers
from .models import Register, Tokens

from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = '__all__'


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = ('email', 'password', 'token', 'id_type', 'banned_type', 'attempt',)


class ConfirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = ('banned_type',)


class ForgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = ('password', 'token',)


class SentForgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = ('token',)


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = (
        'full_name', 'description', 'url_fb', 'url_linkedin', 'url_instagram', 'primary_address', 'primary_phone',
        'email', 'birth_day', 'id_country', 'id_regions', 'id_city', 'url_photo',)


class AttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = ('attempt',)


class PassingAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = ('attempt', 'token',)


class MaxAttemptReachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = ('attempt', 'token', 'password',)


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = ('token',)


class forgetblastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = ('banned_type', 'verfied',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__   '


class V2LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = ('email', 'password', 'token', 'id_type', 'banned_type', 'update_at', 'attempt',)


class TokensSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tokens
        fields = '__all__'


class RegisterFriendsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = ('id', 'email', 'full_name', 'url_photo', 'verfied')


class RegisterlandingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = ('id', 'url_photo', 'ssn_num', 'tax_num', 'primary_phone', 'primary_address')
