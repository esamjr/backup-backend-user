from django.contrib.postgres.fields import ArrayField
from registrations.models import Register
from django.db import models
import datetime


class FeedsObj(models.Model):
    user_id = models.ForeignKey(Register, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=60)
    content = models.TextField()
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    comments_bool = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class Comments(models.Model):
    # user_id = models.IntegerField()
    user_id = models.ForeignKey(Register, on_delete=models.CASCADE)
    feeds_id = models.ForeignKey(FeedsObj, blank=True,
                                 null=True, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=60, blank=False)
    content = models.CharField(max_length=255, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class Likes(models.Model):
    # user_id = models.IntegerField()
    user_id = models.ForeignKey(Register, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=60)
    feeds = models.ManyToManyField(FeedsObj, related_name='user', blank=True)


class Feed(models.Model):
    feed_id = models.ForeignKey(FeedsObj, null=True, on_delete=models.CASCADE)
    feed_content = models.TextField()
    comments = models.ManyToManyField(Comments, blank=True)

    @classmethod
    def instantiate_feeds(cls):
        from .serializers import FeedSerializer
        feed = FeedsObj.objects.latest('id')
        payload = {
            "feed_content": feed.content,
            "feed_id": feed.id
        }
        serializer = FeedSerializer(data=payload)
        if serializer.is_valid():
            serializer.save()

    @classmethod
    def instantiate_comment(cls, feeds_id):
        feed = Feed.objects.filter(feed_id=feeds_id).first()
        feed_comment = Comments.objects.filter(feeds_id=feeds_id)
        feed.comments.add(feed_comment.latest('id'))
