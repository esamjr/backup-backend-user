from django.db import models

# Create your models here.
class FeedsObj(models.Model):	
    content = models.CharField(max_length = 140)
    update_at = models.DateTimeField(auto_now = True)
    user_id = models.IntegerField()
    user_name = models.CharField(max_length = 60)
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    comments_bool = models.BooleanField(default=False)
    comments_content = models.TextField(default="")

class LikesNComments(models.Model):
    feedsobj = models.ForeignKey(FeedsObj, blank=True, null=True, on_delete=models.CASCADE)
    content = models.CharField(max_length=255, blank=False)
    user_id = models.IntegerField(blank=False)
    user_name = models.CharField(max_length = 60, blank=False)

class UserLike(models.Model):
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=60)
    feedsobjs = models.ManyToManyField(FeedsObj, related_name='user_like', blank=True)
