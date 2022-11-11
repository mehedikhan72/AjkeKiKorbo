# Generated by Django 4.1.2 on 2022-11-11 05:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoApp', '0008_remove_review_topic'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='time_zone',
            field=models.CharField(blank=True, default=None, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='reminder',
            name='time',
            field=models.DateField(default=datetime.date(2022, 11, 11)),
        ),
        migrations.AlterField(
            model_name='review',
            name='time',
            field=models.DateField(default=datetime.date(2022, 11, 11)),
        ),
        migrations.AlterField(
            model_name='task',
            name='time',
            field=models.DateField(default=datetime.date(2022, 11, 11)),
        ),
    ]