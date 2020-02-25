from rest_framework import serializers

from employee_sign.models import Employeesign
from hierarchy.models import Hierarchy
from job_contract.models import Jobcontract
from join_company.models import Joincompany
from registrations.models import Register
from .models import Business


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


class NameCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Jobcontract
        fields = '__all__'


class VerBusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ('banned_type',)


class RegIDSerializer(serializers.ModelSerializer):
    class Meta:
        model=Register
        fields = ('id', 'full_name', 'birth_day')


class JoinCompanyIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Joincompany
        fields = ('id_company', )


class JobContractIDSerializer(serializers.ModelSerializer):

    class Meta:
        model = Jobcontract
        fields = ('date_in', 'date_out')


class EmployeeSignIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employeesign
        fields = ('id_contract', )


class HierarchyIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hierarchy
        fields = ('division', )
