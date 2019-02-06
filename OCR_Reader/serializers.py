from rest_framework import serializers
from user_img.models import User_img
from business_img.models import Company_img

class UserImgSerializer(serializers.ModelSerializer):

	class Meta:
		model=User_img
		fields='__all__'

class CompImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company_img
        fields = '__all__'