from django.contrib.auth.models import AbstractUser
from django.db import models
from model_utils import FieldTracker


class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'admin'
        MANAGER = 'manager'
        USER = 'user'

    role = models.CharField(max_length=16, choices=Roles, default=Roles.USER)

    tracker = FieldTracker()

    # TODO: bad pattern, doesn't cover bulk updates
    def save(self, *args, **kwargs):
        if self.pk is None:  # has no ID => not created yet
            # Event.send(name='userCreated`, data=user_data)
            ...
        if self.tracker.has_changed('role'):  # role changed
            # Event.send(name='userRoleChanged`, data=user_data)
            ...

        # Event.send(name='userUpdated', data=user_data)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Event.send(name='userDeleted', data=user_data)
        super().delete(*args, **kwargs)
