from django.db import models
from django.shortcuts import reverse
from django.http import HttpResponseRedirect, HttpResponse

from rest_framework import status
from registrations.models import Register


class Feeds(models.Model):
    user_id = models.ForeignKey(Register, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    @classmethod
    def instantiate_feed_object(cls, feed_instance):
        FeedObject.objects.create(feed_id=feed_instance).save()


class Comments(models.Model):
    user_id = models.ForeignKey(Register, on_delete=models.CASCADE)
    feed_id = models.ForeignKey(
        Feeds, blank=True, null=True, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255, blank=False)
    content = models.CharField(max_length=255, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class Likes(models.Model):
    user_id = models.ForeignKey(Register, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255)
    feeds = models.ManyToManyField(Feeds, related_name='user', blank=True)

    @classmethod
    def instantiate_like_obj(cls, id, user_id):
        from feeds.services import like_feed

        user = Register.objects.filter(id=user_id).first()
        Likes.objects.create(user_id=user, user_name=user.full_name).save()
        like_feed(id=id, user_id=user_id)

class FeedObject(models.Model):
    feed_id = models.ForeignKey(Feeds, on_delete=models.CASCADE, blank=False)
    comments = models.ManyToManyField(Comments, blank=True)
    likes = models.ManyToManyField(Likes, blank=True)

    @classmethod
    def like_feed(cls, u_id, f_id):
        feed = FeedObject.objects.filter(feed_id=f_id).first()
        feed.likes.add(u_id)

    @classmethod
    def unlike_feed(cls, u_id, f_id):
        feed = FeedObject.objects.filter(feed_id=f_id).first()
        feed.likes.remove(u_id)
