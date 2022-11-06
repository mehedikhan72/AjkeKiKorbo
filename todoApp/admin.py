from django.contrib import admin
from .models import Task, User, Reminder

# Register your models here.

admin.site.register(User)
admin.site.register(Task)
admin.site.register(Reminder)
