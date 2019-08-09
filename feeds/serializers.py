from rest_framework import serializers
from .models import FeedsObj, LikesNComments, UserLike


class LikesNCommentsSerializer(serializers.ModelSerializer):
    # feedsobj = FeedsObjSerializer(read_only=False)
    class Meta:
        model = LikesNComments
        fields = '__all__'

class UserLikeSerializer(serializers.ModelSerializer):
    # feedsobj = serializers.PrimaryKeyRelatedField(queryset=FeedsObj.objects.all(), many=True)
    class Meta:
        model = UserLike
        fields = '__all__'

class FeedsObjSerializer(serializers.ModelSerializer):
    # user_like = UserLikeSerializer(many=True, read_only=True)
    class Meta:
        model = FeedsObj
        fields = '__all__'
