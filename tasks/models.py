from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from django_enumfield import enum

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)
    bio = models.TextField(max_length=100)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Label(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.TextField(max_length=24)
	description = models.TextField(max_length=150, blank=True, default='') 
	created_at = models.DateTimeField(default=now)
	
class Task(models.Model):
	name = models.TextField(max_length = 100)
	created_at = models.DateTimeField(default=now)
	due_on = models.DateTimeField()
	status = models.BooleanField()

	class TaskStatus(models.TextChoices):
        NEW = 'N' , _('New Task')
        IN_PROGRESS = 'IP', _('In Progress')
        COMPLETED = 'C', _('Completed')
    status = models.CharField(
        max_length=3,
        choices=TaskStatus.choices,
        default=TaskStatus.NEW,
    )

class TaskLabel(models.Model):
	task = models.ForeignKey(Task)
	label = models.ForeignKey(Label)