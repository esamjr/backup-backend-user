from rest_framework import serializers
from .models import Business
from django.contrib.auth.models import User
from join_company.models import Joincompany
from registrations.models import Register

class RegSerializer(serializers.ModelSerializer):

	class Meta:
		model=Register
		fields='__all__'

class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = '__all__'

class JoincompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Joincompany
        fields = '__all__'

class JoincompanySerializer2(serializers.ModelSerializer):

    class Meta:
        model = Joincompany
        fields = ('id_company',)
