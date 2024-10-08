from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import MaxLengthValidator
from django.utils.translation import gettext_lazy as _

class UserRole(models.TextChoices):
    ADMIN = 'ADMIN', _('Admin')
    USER = 'USER', _('User')

class UserManager(BaseUserManager):
    def create_user(self, username, name, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, name, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):  # Renamed to CustomUser
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, validators=[MaxLengthValidator(255)], blank=False)
    username = models.CharField(max_length=255, unique=True, validators=[MaxLengthValidator(255)], blank=False)
    password = models.CharField(max_length=255, validators=[MaxLengthValidator(255)], blank=False)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=50, choices=UserRole.choices, default=UserRole.USER)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f'User [id={self.id}, name={self.name}, username={self.username}, password={self.password}, active={self.is_active}, role={self.role}]'

    def has_any_authority(self, *authorities):
        return any(self.role == authority for authority in authorities)