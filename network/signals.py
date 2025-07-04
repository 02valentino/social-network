from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FriendRequest, Notification

@receiver(post_save, sender=FriendRequest)
def friend_request_notification(sender, instance, created, **kwargs):
    # Prevent duplicate creation on creation+immediate acceptance
    if created and not instance.accepted:
        # Delete old pending friend requests
        Notification.objects.filter(
            sender=instance.sender,
            recipient=instance.receiver,
            message__icontains="sent you a friend request"
        ).delete()

        Notification.objects.create(
            recipient=instance.receiver,
            sender=instance.sender,
            message=f"{instance.sender.username} sent you a friend request."
        )

    elif instance.accepted:
        # Delete the original friend request notification
        Notification.objects.filter(
            sender=instance.sender,
            recipient=instance.receiver,
            message__icontains="sent you a friend request"
        ).delete()

        # Notify receiver: friendship confirmed
        Notification.objects.create(
            recipient=instance.receiver,
            sender=instance.sender,
            message=f"You and {instance.sender.username} are now friends."
        )

        # Notify sender: request accepted
        Notification.objects.create(
            recipient=instance.sender,
            sender=instance.receiver,
            message=f"{instance.receiver.username} accepted your friend request."
        )
