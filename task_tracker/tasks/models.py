from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    executor = models.ForeignKey(to='users.User', on_delete=models.PROTECT, related_name='tasks_assigned')
    creator = models.ForeignKey(to='users.User', on_delete=models.PROTECT, related_name='tasks_created')
