from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from network.models import FriendRequest

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_banned = models.BooleanField(default=False)  # used by moderators
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    @property
    def friends(self):
        accepted_requests = FriendRequest.objects.filter(
            Q(sender=self) | Q(receiver=self),
            accepted=True
        )
        return [fr.receiver if fr.sender == self else fr.sender for fr in accepted_requests]
