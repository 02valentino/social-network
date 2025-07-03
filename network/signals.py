from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FriendRequest, Notification

@receiver(post_save, sender=FriendRequest)
def friend_request_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.receiver,
            sender=instance.sender,
            message=f"{instance.sender.username} sent you a friend request."
        )
    elif instance.accepted:
        Notification.objects.create(
            recipient=instance.sender,
            sender=instance.receiver,
            message=f"{instance.receiver.username} accepted your friend request."
        )
