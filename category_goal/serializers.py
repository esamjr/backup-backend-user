from rest_framework import serializers
from .models import cat_goal


class CatGoalSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = cat_goal
        fields = '__all__'