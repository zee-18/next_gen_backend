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


class Book(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='books')
    title = models.CharField(max_length=255)
    content = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True)

    def word_count(self):
        return len(self.content.split())

    def __str__(self):
        return self.title
