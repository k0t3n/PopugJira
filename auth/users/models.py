from django.contrib.auth.models import AbstractUser
from django.db import models
from model_utils import FieldTracker

from events.producers import user_producer


class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'admin'
        MANAGER = 'manager'
        USER = 'user'

    role = models.CharField(max_length=16, choices=Roles, default=Roles.USER)

    tracker = FieldTracker()

    # TODO: bad pattern, doesn't cover bulk updates
    def save(self, *args, **kwargs):
        is_created = bool(self.pk is None)
        super().save(*args, **kwargs)
        if is_created:  # has no ID => not created yet
            user_producer.user_created(self)

        if self.tracker.has_changed('role'):  # role changed
            # TODO
            ...

        user_producer.user_updated(self)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        # Event.send(name='userDeleted', data=user_data)
