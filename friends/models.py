from django.db import models
from django.db import IntegrityError
from django.http import JsonResponse
from registrations.models import Register
from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _


class Friends(models.Model):
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=60)
    friend_list = models.ManyToManyField(
        Register, related_name='friend_list', blank=True)
    friend_request = models.ManyToManyField(
        Register, related_name='friend_request', blank=True)
    waiting_for_response = models.ManyToManyField(
        Register, related_name='waiting_for_response', blank=True)

# class Follow(models.Model):
#     user_id = models.IntegerField()
#     user_name = models.CharField(max_length=60)
#     follower = models.ManyToManyField(Register, related_name='follower', blank=True)
#     following = models.ManyToManyField(Register, related_name='following', blank=True)

    # def save(self, *args, **kwargs):
    #     # Ensure users can't be friends with themselves
    #     if self.follower == self.following:
    #         raise JsonResponse("Users cannot follow themselves.")
    #     super(Follow, self).save(*args, **kwargs)
