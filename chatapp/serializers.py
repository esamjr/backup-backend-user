from rest_framework import serializers
from .models import PersonalChat, GroupChat, PersonelGroupChat


class PersonalChatSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PersonalChat
        fields = '__all__'

class GroupChatSerializer(serializers.ModelSerializer):

	class Meta:
		model = GroupChat
		fields = '__all__'

class PersonelSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = PersonelGroupChat
		fields = '__all__'