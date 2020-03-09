from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

# from feeds_register.models import FeedRegister
from registrations.models import Register
from .models import Feeds, FeedObject, CustomUser, Likes, Comments


@receiver(post_save, sender=Register)
def create_custom_user(sender, instance, created, **kwargs):
    """
    after an objects have been save => [post_save],
    auto create custom-user after user created

    :param sender:
    :param instance => Register:
    :param created:
    """
    if created:
        if Register.objects.get(pk=instance.id):
            CustomUser.objects.create(
                user_id=instance, user_name=instance.full_name).save()


@receiver(post_save, sender=Register)
def save_instantiate_like_obj(sender, instance, **kwargs):
    """
    save created custom-user

    :param sender:
    :param instance => Register:
    """
    # instantiate like-obj
    CustomUser.instantiate_like_obj(
        u_id=instance.id, u_name=instance.full_name)


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
