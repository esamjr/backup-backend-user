from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Feeds, FeedObject, Likes, Comments


@receiver(post_save, sender=Feeds)
def create_feed_object(sender, update_fields, created, instance, **kwargs):
    """
    after an objects have been save => [post_save],
    auto create feed-object after user create-feed

    :param sender:
    :param instance => FeedObject:
    :param created:
    """
    if created:
        if update_fields:
            pass
        Feeds.instantiate_feed_object(feed_instance=instance)


@receiver(post_save, sender=Comments)
def update_comments(sender, instance, created, **kwargs):
    if created:
        feed = FeedObject.objects.filter(feed_id=instance.feed_id).first()
        feed_comments = Comments.objects.filter(feed_id=instance.feed_id)
        feed.comments.add(feed_comments.latest('user_id'))
