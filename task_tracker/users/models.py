from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'admin'
        MANAGER = 'manager'
        USER = 'user'

    role = models.CharField(max_length=16, choices=Roles, default=Roles.USER)
