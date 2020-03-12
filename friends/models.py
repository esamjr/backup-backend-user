from django.db import models
from django.db import IntegrityError
from django.http import JsonResponse
from registrations.models import Register
from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _

# CACHE_TYPES = {
#     "followers": "fo-%s",
#     "following": "fl-%s",
#     "blocks": "b-%s",
#     "blocked": "bo-%s",
#     "blocking": "bd-%s",
# }

# BUST_CACHES = {
#     "followers": ["followers"],
#     "following": ["following"],
#     "blocks": ["blocks"],
#     "blocked": ["blocked"],
#     "blocking": ["blocking"],
# }

# def cache_keys(type, user_id):
#     """
#     Build the cache key for a particular type of cached value
#     """
#     return CACHE_TYPES[type] % user_id

# def bust_cache(type, user_id):
#     """
#     Bust our cache for a given type, can bust multiple caches
#     """
#     bust_keys = BUST_CACHES[type]
#     keys = [CACHE_TYPES[k] % user_id for k in bust_keys]
#     cache.delete_many(keys)

class Friends(models.Model):
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=60)
    friend_list = models.ManyToManyField(Register, related_name='friend_list', blank=True)
    friend_request = models.ManyToManyField(Register, related_name='friend_request', blank=True)
    waiting_for_response = models.ManyToManyField(Register, related_name='waiting_for_response', blank=True)

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

