from django.db import models
from registrations.models import Register
from django.db import IntegrityError
from django.http import JsonResponse
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
