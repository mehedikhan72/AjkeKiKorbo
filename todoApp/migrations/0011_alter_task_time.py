# Generated by Django 4.1.2 on 2022-11-11 06:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoApp', '0010_alter_task_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='time',
            field=models.DateField(default=datetime.date(2022, 11, 11)),
        ),
    ]
