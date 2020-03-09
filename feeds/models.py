from django.db import models

from django.http import JsonResponse
from rest_framework import status

from registrations.models import Register


class CustomUser(models.Model):
    user_id = models.ForeignKey(
        Register, on_delete=models.CASCADE, blank=False)
    user_name = models.CharField(max_length=255)

    @classmethod
    def instantiate_like_obj(cls, u_id, u_name):
        user = CustomUser.objects.filter(user_id=u_id).first()
        Likes.objects.create(user_id=user, user_name=u_name).save()


class Feeds(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    @classmethod
    def instantiate_feed_object(cls, feed_instance):
        FeedObject.objects.create(feed_id=feed_instance).save()


class Comments(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    feed_id = models.ForeignKey(
        Feeds, blank=True, null=True, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255, blank=False)
    content = models.CharField(max_length=255, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class Likes(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255)
    feeds = models.ManyToManyField(Feeds, related_name='user', blank=True)


class FeedObject(models.Model):
    feed_id = models.ForeignKey(Feeds, on_delete=models.CASCADE, blank=False)
    comments = models.ManyToManyField(Comments, blank=True)
    likes = models.ManyToManyField(Likes, blank=True)

    @classmethod
    def like_feed(cls, u_id, f_id):
        feed = FeedObject.objects.filter(feed_id=f_id).first()
        feed_likes = Likes.objects.filter(user_id=u_id)
        feed.likes.add(u_id)

    @classmethod
    def unlike_feed(cls, u_id, f_id):
        feed = FeedObject.objects.filter(feed_id=f_id).first()
        feed_likes = Likes.objects.filter(user_id=u_id)
        feed.likes.remove(u_id)
