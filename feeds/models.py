from django.db import models
import datetime

# Create your models here.
class FeedsObj(models.Model):	
    content = models.CharField(max_length = 140)
    update_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.IntegerField()
    user_name = models.CharField(max_length = 60)
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    comments_bool = models.BooleanField(default=False)
    comments_content = models.TextField(default="")

class Comments(models.Model):
    feeds = models.ForeignKey(FeedsObj, blank=True, null=True, on_delete=models.CASCADE)
    content = models.CharField(max_length=255, blank=False)
    user = models.IntegerField(blank=False)
    name = models.CharField(max_length = 60, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Likes(models.Model):
    user = models.IntegerField()
    name = models.CharField(max_length=60)
    feeds = models.ManyToManyField(FeedsObj, related_name='user', blank=True)
