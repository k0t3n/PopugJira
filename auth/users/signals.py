from django.db.models.signals import post_save
from django.dispatch import receiver

from auth.users.models import User


@receiver(post_save, sender=User)
def send_user_changed_event(sender, instance, created, **kwargs):
    if created:
        ...
