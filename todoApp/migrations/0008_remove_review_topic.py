# Generated by Django 4.1.2 on 2022-11-06 11:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todoApp', '0007_review_alter_reminder_time_alter_task_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='topic',
        ),
    ]