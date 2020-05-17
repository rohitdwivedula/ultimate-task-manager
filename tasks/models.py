from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)

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