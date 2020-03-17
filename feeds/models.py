from django.db import models

from rest_framework import status
from registrations.models import Register


class Feeds(models.Model):
    user_id = models.ForeignKey(Register, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def abs_created_at(self):
        return self.created_at.strftime('%B %d, %Y. %H:%M:%S %p')

    def abs_update_at(self):
        return self.update_at.strftime('%B %d, %Y. %H:%M:%S %p')


class Comments(models.Model):
    user_id = models.ForeignKey(Register, on_delete=models.CASCADE)
    feed_id = models.ForeignKey(
        Feeds, blank=True, null=True, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255, blank=False)
    content = models.CharField(max_length=255, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def abs_created_at(self):
        return self.created_at.strftime('%B %d, %Y. %H:%M:%S %p')

    def abs_update_at(self):
        return self.update_at.strftime('%B %d, %Y. %H:%M:%S %p')


class Likes(models.Model):
    user_id = models.ForeignKey(Register, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255)
    feeds = models.ManyToManyField(Feeds, related_name='user', blank=True)

    @classmethod
    def instantiate_like_obj(cls, id, user_id):
        from .services import like_feed

        user = Register.objects.filter(id=user_id)
        if user.exists():
            Likes.objects.create(user_id=user.first(),
                                 user_name=user.first().full_name).save()
        return like_feed(id=id, user_id=user_id)
