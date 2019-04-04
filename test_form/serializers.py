from rest_framework import serializers
from .models import QuestTest, Testform, Testans, answ

class QuestSerializer(serializers.ModelSerializer):
	class Meta:
		model = QuestTest
		fields = '__all__'

class TestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Testform
        fields = '__all__'

class TestansSerializer(serializers.ModelSerializer):

	class Meta:
		model = Testans
		fields = '__all__'

class AnsSerializer(serializers.ModelSerializer):
	class Meta:
		model = answ
		fields = '__all__'
		