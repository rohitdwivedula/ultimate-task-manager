"""Helper module for various other class/functions in authentication app"""
import random

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.template.loader import render_to_string
from django.utils import timezone

from authentication.models import User
from tasks.models import Label, Task, SubTask

class UserHelper:
    """Helper methods related to User registration and authentication"""
    @staticmethod
    def generate_token(n):
        dictionary = "1234567890"
        token = ""
        for i in range(0, n):
            token += dictionary[random.randrange(0, len(dictionary))]
        return token

    @staticmethod
    def create_user(email, password, **kwargs):
        user = User(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    @staticmethod
    def update_user_password(user, password):
        user.set_password(password)
        user.save()

    @staticmethod
    def check_user_exists(email):
        try:
            user = User.objects.get(email=email)
            return user
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            return None

    @staticmethod
    def check_user_credentials(user, password):
        try:
            if user.check_password(password):
                return True
            return False
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def _set_new_verification_token(user, token_length, ttl, force_set=False, save_user=True, numbers_only=False):
        """Sets a new user token of given length
        * `token_length` is the length of the token
        * `ttl` determines how long (in seconds) the previously set token is
           valid for before setting a new one
        * `force_set` forces a new token to be set irrespective of ttl
        """
        if not force_set:
            timediff = (timezone.now() - user.generated_at).total_seconds()
            if not (timediff > ttl):
                return False  # don't set token again

        user.verification_token = UserHelper.generate_token(token_length)
        user.generated_at = timezone.now()

        if save_user:
            user.save()
        return True

    @staticmethod
    def set_new_activation_token(user, force_set=False, save_user=False):
        """Sets a new activation token
        Returns true if activation token has been successfully set
        """
        return UserHelper._set_new_verification_token(user, 64, 1800, force_set, save_user)

    @staticmethod
    def set_new_forgot_password_token(user, force_set=False, save_user=False):
        return UserHelper._set_new_verification_token(user, 8, 600, force_set=force_set, save_user=save_user,
                                                      numbers_only=True)

    @staticmethod
    def send_activation_email(user, request):
        link_format = '/api/auth/verify?email={}&token={}'.format(user.email, user.verification_token)
        activation_link = request.build_absolute_uri(link_format)
        message = "Please click this link to activate your account: " + activation_link + " \n\n\nThanks for registering!"
        user.email_user("Ultimate Task Manager - Activate Your Account", message)

    @staticmethod
    def send_forgot_password_token_email(user, request):
        verification_token_str = str(user.verification_token)
        message = "Your One Time Password is: " + verification_token_str + "\n\nDO NOT SHARE THIS OTP."
        user.email_user("Ultimate Task Manager - Forgot Password", message)

    @staticmethod
    def user_onboarding(user, request):
        label_names = ["Work", "Shopping", "Personal"]
        descriptions = ["Plan career related stuff here.", "From vegetables to that pending car repair.", "Everything about your life at home."]
        for i in range(0, len(label_names)):
            label_obj = Label(user=user, name=label_names[i], description=descriptions[i])
            print(label_obj)
            label_obj.save()
        sample_task = Task(user=user, name = "Welcome to Ultimate! [Tutorial]", \
            desc = "Use ultimate to plan your work, chores and play - create tasks, attach sub-goals to tasks and set due dates.")
        sample_task.save() # you cannot add a label unless the task is saved
        sample_task.labels.add(label_obj)
        sample_task.save()
        subtask_names = ["Try creating a new task", "Manage labels by creating a new label or editing an existing one", "Create subtasks and mark them as complete", "Delete this task once you're done"]
        for subtask_name in subtask_names:
            subtask = SubTask(name=subtask_name, task=sample_task)
            print(subtask)
            subtask.save()
