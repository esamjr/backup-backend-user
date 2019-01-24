from rest_framework import serializers
from .models import Business
from django.contrib.auth.models import User
from join_company.models import Joincompany
from registrations.models import Register

class RegSerializer(serializers.ModelSerializer):

	class Meta:
		model=Register
		fields='__all__'

class CustomJoincompanySerializer(serializers.ModelSerializer):
    # id_user = RegSerializer(many=True, read_only=True)
    id_user = serializers.ReadOnlyField(source='Register.full_name')
    class Meta:
        model = Joincompany
        fields = '__all__'



class BusinessSerializer(serializers.ModelSerializer):
    # name = serializers.ReadOnlyField(source='Business.username')
    class Meta:
        model = Business
        #field = ('id_user','company_name','email','primary_phone','primary_address','id_country','id_regions','id_city','id_business_type','tax_num','logo_path','description','id_type','banned_type','create_at','update_at','delete_at')
        fields = '__all__'

class JoincompanySerializer(serializers.ModelSerializer):
    # id_company = BusinessSerializer(many=True, read_only=True)
    class Meta:
        model = Joincompany
        fields = '__all__'

class JoincompSerializer(serializers.ModelSerializer):
    id_company = BusinessSerializer(many=False, read_only=True)

    class Meta:
        model = Joincompany
        fields = '__all__'

# class JoincompSerializer(serializers.ModelSerializer):
#     id_company = JoincompanySerializer(many=True, read_only=True)
#     class Meta:
#         model = Business
#         #field = ('id_user','company_name','email','primary_phone','primary_address','id_country','id_regions','id_city','id_business_type','tax_num','logo_path','description','id_type','banned_type','create_at','update_at','delete_at')
#         fields = '__all__'

class SearchSerializer(serializers.ModelSerializer):
    # Business = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    # id_company = JoincompanySerializer(many = True, read_only=True)
    # id_company = Joincompany.objects.all().filter(status="1")
    # id_company = serializers.ReadOnlyField(source='Joincompany')
    id_company = JoincompanySerializer(source='id_company')

    class Meta:
        model = Joincompany
        fields = ('id_company', 'company_name')

        def create(self, validated_data):
            business_data = validated_data.pop('id_company')
            try:
                business_instance = BUsiness.objects.filter(**business_data)[0]
            except IndexError:
                business_instance = Bussines.objects.create(**business_data)
            return Joincompany.objects.create(id_company=business_instance, **validated_data)



# class TrackSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Track
#         fields = ('order', 'title', 'duration')

# class AlbumSerializer(serializers.ModelSerializer):
#     tracks = TrackSerializer(many=True, read_only=True)

#     class Meta:
#         model = Album
#         fields = ('album_name', 'artist', 'tracks')\