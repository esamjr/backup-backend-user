from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from .models import Feeds, Likes, Comments

from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@receiver([post_save, post_delete], sender=Feeds)
@receiver([post_save, post_delete], sender=Comments)
@receiver([post_save, post_delete], sender=Likes)
def delete_cache(sender, **kwargs):
    from .services import feed_as_object
    if sender:
        cache.delete_pattern("*")

        # create new cache
        page = 1
        feed_page_x = f'feed_page_{page}'
        paginated_feed, page_len = feed_as_object(page=page)
        cache.set(feed_page_x, paginated_feed, timeout=CACHE_TTL)
        cache.set('page_len', page_len, timeout=CACHE_TTL)
