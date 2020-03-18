from django.db import models

from registrations.models import Register
from django.contrib.auth.models import User


class Friends(models.Model):
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=60)
    friend_list = models.ManyToManyField(Register, related_name='friend_list', blank=True)
    friend_request = models.ManyToManyField(Register, related_name='friend_request', blank=True)
    waiting_for_response = models.ManyToManyField(Register, related_name='waiting_for_response', blank=True)
    blocker_to = models.ManyToManyField(Register, related_name='blocker_to', blank=True)
    blocked_by = models.ManyToManyField(Register, related_name='blocked_by', blank=True)