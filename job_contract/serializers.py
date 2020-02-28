from rest_framework import serializers
from .models import Jobcontract
from django.contrib.auth.models import User


class JobcontractSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='name.username')

    class Meta:
        model = Jobcontract
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    User = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = User
        fields = '__all__'


class JobContractIDSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='name.username')

    class Meta:
        model = Jobcontract
        fields = ('id_company', 'id_user', 'id_contract', 'salary', 'date_in', 'date_out', 'status')
