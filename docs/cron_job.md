To send reminder emails/Discord messages to all users a custom management command `send_reminders` has been setup in Django. A shell script has been created in `/cronjobs` of this repo as a wrapper for this python function.

Add an entry to your system's `CRON` table by running the command `crontab -e` and appending this line to the file:

```
00 9 * * * /home/rohit/ultimate-task-manager/cronjobs/reminders.sh
```

This will ensure email updates are triggered at 9:00AM every day. Please note that you need to provide the absolute file path both in this `crontab` entry and in the `cronjobs/reminders.sh` file - replace `/home/rohit/` with the path to your working repo directory