from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Follow, Notification

@receiver(post_save, sender=Follow)
def create_follow_notification(sender, instance, created, **kwargs):
    if created:
        follower = instance.follower
        following = instance.following
        if follower != following:
            Notification.objects.create(
                recipient=following,
                sender=follower,
                message=f"{follower.username} started following you."
            )
