from tkinter import CASCADE
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import datetime
# Create your models here.

class User(AbstractUser):
    pass

class Task(models.Model):
    name = models.TextField(max_length=256)
    creator = models.CharField(max_length=64, null=True, blank=True)
    time = models.DateField(default=datetime.date.today())
    importance = models.PositiveIntegerField(default=3)
    completed = models.BooleanField(default=False)


