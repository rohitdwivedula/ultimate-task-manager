from django.db import models
from django.utils.timezone import now
from authentication.models import User
 
class Label(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.TextField(max_length=24)
    description = models.TextField(max_length=150, blank=True) 
    created_at = models.DateTimeField(default=now)
    
class Task(models.Model):
    name = models.TextField(max_length = 100)
    created_at = models.DateTimeField(default=now)
    due_on = models.DateTimeField()
    status = models.BooleanField()
    labels = models.ManyToManyField(Label)

    class TaskStatus(models.TextChoices):
        NEW = 'N', 'NEW TASK'
        IN_PROGRESS = 'IP', 'IN PROGRESS'
        COMPLETED = 'C', 'COMPLETED'

    status = models.CharField(
        max_length=3,
        choices=TaskStatus.choices,
        default=TaskStatus.NEW,
    )

class SubTask(models.Model):
    description = models.TextField(max_length = 128)
    class SubTaskStatus(models.TextChoices):
        DONE = 'D', 'DONE'
        NOT_DONE = 'ND', 'NOT DONE' 
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=3,
        choices=SubTaskStatus.choices,
        default = SubTaskStatus.NOT_DONE
    )