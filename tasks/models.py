from authentication.models import User
from django.db import models
from django.utils.timezone import now

class Label(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField(max_length=24, verbose_name='Label Name')
    description = models.TextField(max_length=150, blank=True) 
    created_at = models.DateTimeField(default=now)

    def __str__(self):
    	return self.user.first_name.lower() + "_" + self.name
    
class Task(models.Model):
    name = models.TextField(max_length = 100, verbose_name='Task Heading')
    desc = models.TextField(max_length = 1000, verbose_name='Task Description')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name = 'Created By')
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

    def __str__(self):
    	return self.user.first_name.lower() + "_" + self.name

class SubTask(models.Model):
    name = models.TextField(max_length = 128, verbose_name='Subtask description')
    class SubTaskStatus(models.TextChoices):
        DONE = 'D', 'DONE'
        NOT_DONE = 'ND', 'NOT DONE' 
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=3,
        choices=SubTaskStatus.choices,
        default = SubTaskStatus.NOT_DONE
    )

    def __str__(self):
    	return self.task.user.first_name.lower() + "_" + self.task.name