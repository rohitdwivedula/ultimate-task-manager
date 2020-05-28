from django.db import models
from django.utils.translation import gettext_lazy as _

class TaskStatus(models.TextChoices):
    NEW = 'N', _('NEW TASK')
    IN_PROGRESS = 'IP', _('IN PROGRESS')
    COMPLETED = 'C', _('COMPLETED')

class SubTaskStatus(models.TextChoices):
    DONE = 'D', _('DONE')
    NOT_DONE = 'ND', _('NOT DONE') 