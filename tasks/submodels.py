from django.db import models
from django.utils.translation import gettext_lazy as _

class TaskStatus(models.TextChoices):
    NEW = 'N', _('NEW TASK')
    IN_PROGRESS = 'I', _('IN PROGRESS')
    COMPLETED = 'C', _('COMPLETED')

class SubTaskStatus(models.TextChoices):
    DONE = 'D', _('DONE')
    NOT_DONE = 'ND', _('NOT DONE')

class Priority(models.TextChoices):
	LOW = 'L', _('LOW')
	MEDIUM = 'M', _('MEDIUM')
	HIGH = 'H', _('HIGH')
