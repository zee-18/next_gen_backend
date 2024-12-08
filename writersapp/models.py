from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    VIEWER = 'viewer', 'Viewer'
    EDITOR = 'editor', 'Editor'

class CustomUser(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.VIEWER,
    )
