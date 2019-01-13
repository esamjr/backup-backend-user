from rest_framework import serializers
from .models import Business
from django.contrib.auth.models import User

class BusinessSerializer(serializers.ModelSerializer):
    #name = serializers.ReadOnlyField(source='Business.username')
    class Meta:
        model = Business
        #field = ('id_user','company_name','email','primary_phone','primary_address','id_country','id_regions','id_city','id_business_type','tax_num','logo_path','description','id_type','banned_type','create_at','update_at','delete_at')
        fields = '__all__'

"""class UserSerializer(serializers.ModelSerializer):
    Business = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = User
        fields = '__all__'"""