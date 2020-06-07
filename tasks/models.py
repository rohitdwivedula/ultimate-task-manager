from authentication.models import User
from django.db import models
from django.utils.timezone import now
from tasks.submodels import TaskStatus, SubTaskStatus, Priority
import uuid

class Label(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField(max_length=24, verbose_name='Label Name')
    description = models.TextField(max_length=150, blank=True) 
    created_at = models.DateTimeField(default=now)

    def __str__(self):
    	return self.user.first_name.lower() + "_" + self.name
    
class Task(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name = 'Created By')
    name = models.TextField(max_length = 100, verbose_name='Task Heading')
    desc = models.TextField(max_length = 1000, verbose_name='Task Description')
    created_at = models.DateTimeField(default=now)
    due_on = models.DateTimeField(default=now)
    status = models.BooleanField()
    priority = models.CharField(
        max_length=2,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )
    labels = models.ManyToManyField(Label)
    status = models.CharField(
        max_length=3,
        choices=TaskStatus.choices,
        default=TaskStatus.NEW,
    )

    def __str__(self):
    	return self.user.first_name.lower() + "_" + self.name

class SubTask(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.TextField(max_length = 128, verbose_name='Subtask description')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="subtasks")
    status = models.CharField(
        max_length=3,
        choices=SubTaskStatus.choices,
        default = SubTaskStatus.NOT_DONE
    )
    created_at = models.DateTimeField(default=now)

    def __str__(self):
    	return self.task.user.first_name.lower() + "_" + self.task.name

    class Meta:
        ordering = ['created_at']