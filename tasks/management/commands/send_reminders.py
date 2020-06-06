from django.core.management.base import BaseCommand, CommandError
from authentication.models import User
from tasks.models import Label, Task, SubTask 
import datetime
import requests

class Command(BaseCommand):
    help = 'Trigger email reminders to users'

    def handle(self, *args, **options):
        all_users = User.objects.all()
        for user in all_users:
            if user.discord_notifications_enabled or user.email_notifications_enabled:
                days = user.remind_duration
                filter_date = datetime.date.today() + datetime.timedelta(days=days)
                tasks = Task.objects.filter(user=user, due_on__date=filter_date)
                if tasks:
                    subject = "Today's Reminders: " + str(datetime.date.today())
                    message = "You have " + str(len(tasks)) + " task(s) due on " + str(filter_date) + "\n\n"
                    i = 1
                    for task in tasks:
                        message += "\n" + str(i) + ". " + task.name + "\n"
                        if len(task.desc) != 0: 
                            message += "Description: " + task.desc
                        message += "\n\n"
                        i += 1
                    if user.email_notifications_enabled:
                        user.email_user(subject, message)
                        self.stdout.write(self.style.SUCCESS('Emailed "%s" a reminder.' % user.email))
                    if user.discord_notifications_enabled:
                        try:
                            url = user.discord_webhook_url
                            content = {
                                'username': 'Ultimate Tasks | Reminder',
                                'content': message
                            }
                            response = requests.post(url, data = content)
                            print(response)
                            if response.status_code in [200, 204]:
                                self.stdout.write(self.style.SUCCESS('Discord message sent to "%s" a reminder.' % user.email))
                            else:
                                self.stdout.write(self.style.ERROR('Discord message could not be sent to "%s".' % user.email))
                        except requests.exceptions.ConnectionError:
                            self.stdout.write(self.style.ERROR('Discord message could not be sent to "%s". URL: %s' % (user.email, user.discord_webhook_url)))
                else:
                    self.stdout.write(self.style.SUCCESS('No notifications needed for "%s".' % user.email))
            else:
                self.stdout.write(self.style.SUCCESS('Reminder updates not enabled for "%s"' % user.email))