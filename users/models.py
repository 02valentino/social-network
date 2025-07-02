from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_banned = models.BooleanField(default=False)  # used by moderators
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.username