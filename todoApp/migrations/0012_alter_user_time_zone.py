# Generated by Django 4.1.2 on 2022-11-11 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoApp', '0011_alter_task_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='time_zone',
            field=models.CharField(default='UTC', max_length=128),
        ),
    ]
