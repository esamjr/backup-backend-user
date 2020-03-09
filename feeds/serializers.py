from rest_framework import serializers
from feeds.models import Feeds, Comments, Likes, FeedObject


class FeedsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feeds
        fields = '__all__'


class FeedObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedObject
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = '__all__'
