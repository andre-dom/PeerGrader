from django.db import models
from django.contrib.auth.models import AbstractUser


# custom user class
class AppUser(AbstractUser):
    is_instructor = models.BooleanField(default=False)
