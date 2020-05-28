# Generated by Django 3.0.6 on 2020-05-28 09:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=24, verbose_name='Label Name')),
                ('description', models.TextField(blank=True, max_length=150)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=100, verbose_name='Task Heading')),
                ('desc', models.TextField(max_length=1000, verbose_name='Task Description')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('due_on', models.DateTimeField()),
                ('status', models.CharField(choices=[('N', 'NEW TASK'), ('IP', 'IN PROGRESS'), ('C', 'COMPLETED')], default='N', max_length=3)),
                ('labels', models.ManyToManyField(to='tasks.Label')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
            ],
        ),
        migrations.CreateModel(
            name='SubTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=128, verbose_name='Subtask description')),
                ('status', models.CharField(choices=[('D', 'DONE'), ('ND', 'NOT DONE')], default='ND', max_length=3)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.Task')),
            ],
        ),
    ]
