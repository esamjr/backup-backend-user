from rest_framework import serializers
from .models import FeedsObj, Comments, Likes


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'

class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = '__all__'

class FeedsObjSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedsObj
        fields = '__all__'
