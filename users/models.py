from django.db import models
from django.contrib.auth.models import AbstractUser
from shared.models import BaseModel

class CustomUser(AbstractUser, BaseModel):
    profile_picture = models.ImageField(default="profile_default_picture.jpg", upload_to='profile_image')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
