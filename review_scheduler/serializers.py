from rest_framework import serializers
from .models import review_scheduler


class ReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = review_scheduler
        fields = '__all__'
