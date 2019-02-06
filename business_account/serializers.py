from rest_framework import serializers
from .models import Business
from django.contrib.auth.models import User
from join_company.models import Joincompany
from registrations.models import Register
from job_contract.models import Jobcontract

class RegSerializer(serializers.ModelSerializer):

	class Meta:
		model=Register
		fields=('id','full_name','birth_day','email','primary_phone','primary_address','id_country','id_city','id_regions','url_fb','url_linkedin','url_instagram',)

class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = '__all__'

class JoincompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Joincompany
        fields = '__all__'

class JobconSerializer(serializers.ModelSerializer):

    class Meta:
        model = Jobcontract
        fields = '__all__'
