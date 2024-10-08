from django.db import models
from django.contrib.auth.models import AbstractUser

class UserRole(models.TextChoices):
    ADMIN = 'ADMIN', 'Administrator'
    MODER = 'MODER', 'Moderator'

class UserRoleUser(AbstractUser):  # Renamed to UserRoleUser
    role = models.CharField(
        max_length=5,
        choices=UserRole.choices,
        default=UserRole.MODER,
    )

    def get_role_display(self):
        return self.get_role_display()