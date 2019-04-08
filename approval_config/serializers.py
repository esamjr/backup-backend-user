from rest_framework import serializers
from .models import Approval
# from django.contrib.auth.models import User

class ApprovalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Approval
        fields = '__all__'