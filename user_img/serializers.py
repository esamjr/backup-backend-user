from rest_framework import serializers
from registrations.models import Register


class ValidSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Register
        fields = ('ssn_num', 'verfied',)

class ExpTaxnumSerializer(serializers,ModelSerializer):
	class Mete:
		model = Register
		fields = ('tax_num',)
