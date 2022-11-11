from logging import log
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from . models import User, Task, Reminder, Review
import datetime, calendar
import random
import json
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
import pytz

# Create your views here.

def index(request):
    return render(request, "todoApp/index.html")
    
@login_required
def today(request):
    user = request.user
    current_date = datetime.datetime.now(pytz.timezone(user.time_zone)).date()
    
    tasks = Task.objects.filter(creator=user, time=current_date).values()

    total_tasks = tasks.count()
    pending_tasks = Task.objects.filter(creator=user, time=current_date, completed=False).count()
    completed_tasks = total_tasks - pending_tasks

    rem = Reminder.objects.filter(creator=user).values()
    rem_list = []
    if rem:
        for r in rem:
            rem_list.append(r["name"])

        temp = random.randint(0, len(rem_list) - 1)
        sent_reminder = rem_list[temp]
    else:
        sent_reminder = None

    # Getting yesterdays unfinished tasks!
    yesterday = current_date - datetime.timedelta(1)
    yesterday_tasks = Task.objects.filter(creator=user, time=yesterday).values()

    if yesterday_tasks:
        yesterday_total_tasks = yesterday_tasks.count()
        yesterday_pending_tasks = Task.objects.filter(creator=user, time=yesterday, completed=False).count()
        yesterday_completed_tasks = yesterday_total_tasks - yesterday_pending_tasks
    
        yesterday_completion_percentagee = round((yesterday_completed_tasks / yesterday_total_tasks) * 100)
    else:
        yesterday_completion_percentagee = None

    # Sending email if user has not schedule tasks for the next day and it's already 11 PM.
    
    return render(request, "todoApp/today.html", {
        "tasks" : tasks,
        "total_tasks" : total_tasks,
        "pending_tasks" : pending_tasks,
        "completed_tasks" : completed_tasks,
        "reminder" : sent_reminder,
        "yesterday_tasks" : yesterday_tasks,
        "yesterday_completion_percentage" : yesterday_completion_percentagee
    })    

@login_required
def tomorrow(request):
    user = request.user
    current_date = datetime.datetime.now(pytz.timezone(user.time_zone)).date()
    tomorrow_date = current_date + datetime.timedelta(1)
    tasks = Task.objects.filter(creator=user, time=tomorrow_date).values()

    rem = Reminder.objects.filter(creator=user).values()
    rem_list = []

    if rem:
        for r in rem:
            rem_list.append(r["name"])

        temp = random.randint(0, len(rem_list) - 1)
        sent_reminder = rem_list[temp]
    else:
        sent_reminder = None
        
    return render(request, "todoApp/tomorrow.html", {
        "tasks" : tasks,
        "reminder" : sent_reminder,

    })


@login_required
def add_task(request, day):
    user = request.user
    if request.method == 'POST':
        task = request.POST["task"]
        creator = str(request.user)
        if day == 'today':
            time = current_date = datetime.datetime.now(pytz.timezone(user.time_zone)).date()
        elif day == 'tomorrow':
            time = current_date = datetime.datetime.now(pytz.timezone(user.time_zone)).date() + datetime.timedelta(1)

        if not task:
            return render(request, "todoApp/error.html", {
                "message" : "Task must not be empty!"
            })

        new_task = Task.objects.create(name=task, creator=creator, time=time)   
        new_task.save() 


        if day == 'today':
            return HttpResponseRedirect(reverse("today"))
        elif day == 'tomorrow':
            return HttpResponseRedirect(reverse("tomorrow"))

    else:
        return render(request, "todoApp/add_task.html", {
            "day" : day,
        })

@login_required
def complete_task(request, id):
    task = Task.objects.get(id=id)
    task.completed = True
    task.save()

    return HttpResponseRedirect(reverse("today"))

@login_required
def delete_task(request, id, day):
    task = Task.objects.get(id=id)
    task.delete()

    if day == 'today':
        return HttpResponseRedirect(reverse("today"))
    elif day == 'tomorrow':
        return HttpResponseRedirect(reverse('tomorrow'))

@login_required
def progress(request):
    user = request.user
    current_date = current_date = datetime.datetime.now(pytz.timezone(user.time_zone)).date()
    if request.method == "POST":
        try:
            current_month = int(request.POST["month"])
            current_year = int(request.POST["year"])
        except ValueError:
            return render(request, "todoApp/error.html", {
                "message" : "Please enter valid data!"
            })           

        if current_month > 12 or current_month < 1:
            return render(request, "todoApp/error.html", {
                "message" : "Please enter a valid month[From 1 to 12]!"
            })
        
        if current_year > 9999:
            return render(request, "todoApp/error.html", {
                "message" : "Did you time travel to the future or something?"
            })

    else:
        current_month = current_date.month
        current_year = current_date.year

    num_days = calendar.monthrange(current_year, current_month)[1]
    this_month = [datetime.date(current_year, current_month, day) for day in range(1, num_days + 1)]

    tomorrow = current_date + datetime.timedelta(1)

    if current_date in this_month:
        this_month.remove(current_date)
    
    if tomorrow in this_month:
        this_month.remove(tomorrow)

    existing_days = []
    tasks = Task.objects.filter(creator=user, time__in=this_month).order_by('-id')
    for task in tasks:
        if task.time not in existing_days:
            existing_days.append(task.time)

    # Storing the total and completed count of this month(existing days) in the two following lists.
    total_tasks = []
    completed_tasks = []
    for day in existing_days:
        task_count = Task.objects.filter(creator=user, time=day).count()
        total_tasks.append(task_count)
        completed_count = Task.objects.filter(creator=user, time=day, completed=True).count()
        completed_tasks.append(completed_count)

    scores = []
    for i in range(len(existing_days)):
        scores.append(str(completed_tasks[i]) + '/' + str(total_tasks[i]))


    bg_color = []
    border_color = []
    verdicts = []
    complete_percentage = []
    for i in range(len(existing_days)):
        points = completed_tasks[i] / total_tasks[i]
        complete_percentage.append(points * 100)
        if points >= 0.9:
            verdicts.append("Fantastic Day!")
            bg_color.append("rgba(1, 195, 1, 0.2)")
            border_color.append("rgba(1, 195, 1, 1)")
        
        elif points >= 0.75:
            verdicts.append("Nice Work!")
            bg_color.append("rgba(9, 141, 9, 0.2)")
            border_color.append("rgba(9, 141, 9, 1)")

        elif points >= 0.50:
            verdicts.append("Try Harder!")
            bg_color.append("rgba(199, 186, 8, 0.2)")
            border_color.append("rgba(199, 186, 8, 1)")
        
        elif points >= 0.25:
            verdicts.append("Do Better!")
            bg_color.append("rgba(197, 112, 0, 0.2)")
            border_color.append("rgba(197, 112, 0, 1)")
        
        else:
            verdicts.append("Are You Ok?")
            bg_color.append("rgba(251, 2, 2, 0.2)")
            border_color.append("rgba(251, 2, 2, 1)")

    complete_percentage = complete_percentage[::-1]
    bg_color = bg_color[::-1]
    border_color = border_color[::-1]

    labels = []
    for d in existing_days:
        d = str(d)
        labels.append(d)

    labels = labels[::-1]

    rem = Reminder.objects.filter(creator=user).values()
    rem_list = []
    if rem:
        for r in rem:
            rem_list.append(r["name"])

        temp = random.randint(0, len(rem_list) - 1)
        sent_reminder = rem_list[temp]
    else:
        sent_reminder = None

    return render(request, "todoApp/progress.html", {
        "existing_days" : existing_days,
        "scores" : scores,
        "verdicts" : verdicts,
        "complete_percentage" : complete_percentage,
        "labels" : labels,
        "bg_color" : bg_color,
        "border_color" : border_color,
        "reminder" : sent_reminder,
    })

def reminder(request):
    user = str(request.user)
    if request.method == "POST":
        name = request.POST["reminder"]

        if not name:
            return render(request, "todoApp/error.html", {
                "message" : "Reminder must not be empty!"
            })

        rem = Reminder.objects.create(name=name, creator=user)
        rem.save()
        return HttpResponseRedirect(reverse("reminder"))
    
    reminders = Reminder.objects.filter(creator=user)

    return render(request, "todoApp/reminders.html", {
        "reminders" : reminders,
    })

def delete_reminder(request, id):
    ajke_rubaiyat_er_bday = Reminder.objects.get(id=id)
    ajke_rubaiyat_er_bday.delete()

    return HttpResponseRedirect(reverse("reminder"))

def details(request, date):
    user = request.user
    try:
        tasks = Task.objects.filter(creator=user, time=date).values()
    except ValidationError:
            return render(request, "todoApp/error.html", {
                "message" : "Page Not Found!"
            })

    return render(request, "todoApp/details.html", {
        "tasks" : tasks,
        "date" : date,
    })

def add_review(request):
    user = str(request.user)
    rev = json.load(request)["review"]

    if not rev:
        return render(request, "todoApp/error.html", {
            "message" : "Review must not be empty!"
        })

    review = Review.objects.create(rev=rev, creator=user)
    review.save()

    return HttpResponse("review added!")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "todoApp/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "todoApp/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        time_zone = request.POST.get("timezone")
        print(time_zone)

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "todoApp/register.html", {
                "message": "Passwords must match."
            })
        
        if not time_zone:
            return render(request, "todoApp/register.html", {
                "message": "Passwords enter a timezone."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, time_zone=time_zone)
            user.save()
        except IntegrityError:
            return render(request, "todoApp/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        # Send mail to user
        subject = "Welcome text for registration."
        message = "Thank you for registering to 'AjkeKiKorbo'. We hope you find this web application useful in your day to day life. Feel free to contact us via the review section in the app's homepage or this email. Happy Grinding!"
        sender = 'ajkekikorbo0@gmail.com'
        recipient = [ user.email ]

        send_mail(subject, message, sender, recipient, fail_silently=False)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "todoApp/register.html", {
            'timezones' : pytz.common_timezones,
        })

