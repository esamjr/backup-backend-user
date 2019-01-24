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
    id_user = serializers.ReadOnlyField(source='Register')
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

class SearchSerializer(serializers.ModelSerializer):
    # Business = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    # id_company = JoincompanySerializer(many = True, read_only=True)
    # id_company = Joincompany.objects.all().filter(state="1")
    id_company = serializers.ReadOnlyField(source='Joincompany')
    class Meta:
        model = Business
        fields = ('id_company', 'company_name')
# class TrackSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Track
#         fields = ('order', 'title', 'duration')

# class AlbumSerializer(serializers.ModelSerializer):
#     tracks = TrackSerializer(many=True, read_only=True)

#     class Meta:
#         model = Album
#         fields = ('album_name', 'artist', 'tracks')\