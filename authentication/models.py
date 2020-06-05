from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.timezone import now
from django.conf import settings
from django.core.mail import send_mail
from django.core.validators import MaxValueValidator, MinValueValidator

class UserManager(BaseUserManager):
    """
    UserManager class for assisting create user, superuser methods while migrating.
    """
    def create_user(self, email, password, first_name, last_name, ip_address, mac_address, location):
        """Create a user. Overides the default implementation"""
        user = self.model(email=self.normalize_email(email), first_name=first_name, last_name=last_name,
                          ip_address=ip_address)
        user.set_password(password)
        user.is_verified = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Create a superuser. Overrides the default implemetation"""
        user = self.create_user(email=email, password=password, first_name=None, last_name=None, ip_address=None,
                                mac_address=None, location=None)
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """
        The main User database model that extends AbstractUser class with 
        additional fields:
            * first_name, last_name -- name
            * ip_address -- IP address
            * location -- location as a string "lat,long"
            * date_joined -- date of registration, set during object creation
            * is_verified -- whether user had done email verification
            * verification_token -- token used to activate email and reset passwords
            * generated_at -- time at which `verification_token` was generated
    """
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    date_joined = models.DateTimeField(default=now, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    two_factor_enabled = models.BooleanField(default=False)

    email_notifications_enabled = models.BooleanField(default=False)
    discord_notifications_enabled = models.BooleanField(default=False)
    discord_webhook_url = models.URLField(default='')
    remind_duration = models.PositiveIntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(100)])

    verification_token = models.CharField(max_length=64, blank=True, null=True)
    generated_at = models.DateTimeField(null=True, blank=True)

    bio = models.TextField(max_length=280, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        """Return first_name and last_name with a whitespace in between."""
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the shortname"""
        return self.first_name

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Return true if user has a specified permission."""
        return self.is_superuser

    @property
    def is_staff(self):
        """Return true if the user a staff member."""
        return self.is_superuser

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=False,
        )