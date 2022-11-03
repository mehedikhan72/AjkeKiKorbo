from logging import log
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from . models import User, Task
import datetime, calendar

# Create your views here.

def index(request):
    return render(request, "todoApp/index.html")
    

@login_required
def today(request):
    user = request.user
    current_date = datetime.date.today()
    tasks = Task.objects.filter(creator=user, time=current_date).values().order_by('-importance')

    total_tasks = tasks.count()
    pending_tasks = Task.objects.filter(creator=user, time=current_date, completed=False).count()
    completed_tasks = total_tasks - pending_tasks

    return render(request, "todoApp/today.html", {
        "tasks" : tasks,
        "total_tasks" : total_tasks,
        "pending_tasks" : pending_tasks,
        "completed_tasks" : completed_tasks,
    })

@login_required
def tomorrow(request):
    user = request.user
    current_date = datetime.date.today()
    tomorrow_date = current_date + datetime.timedelta(1)
    tasks = Task.objects.filter(creator=user, time=tomorrow_date).values().order_by('-importance')

    return render(request, "todoApp/tomorrow.html", {
        "tasks" : tasks
    })


@login_required
def add_task(request, day):
    if request.method == 'POST':
        task = request.POST["task"]
        importance = request.POST["importance"]
        creator = str(request.user)
        if day == 'today':
            time = datetime.date.today()
        elif day == 'tomorrow':
            time = datetime.date.today() + datetime.timedelta(1)

        new_task = Task.objects.create(name=task, creator=creator, time=time, importance=importance)   
        new_task.save() 

        # if request.POST["save"] == 'save_add_another':
        #     return render(request, "todoApp/add_task.html", {
        #         "day" : day,
        #     })

        # elif request.POST["save"] == 'save':
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
    print(task)
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
    current_date = datetime.date.today()
    if request.method == "POST":
        current_month = int(request.POST["month"])
        current_year = int(request.POST["year"])

    else:
        current_month = current_date.month
        current_year = current_date.year

    user = request.user

    num_days = calendar.monthrange(current_year, current_month)[1]
    this_month = [datetime.date(current_year, current_month, day) for day in range(1, num_days + 1)]

    existing_days = []
    tasks = Task.objects.filter(creator=user, time__in=this_month).order_by('-id')
    for task in tasks:
        if task.time not in existing_days:
            existing_days.append(task.time)

    if existing_days:
        existing_days.remove(current_date)

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

    verdicts = []
    for i in range(len(existing_days)):
        points = completed_tasks[i] / total_tasks[i]
        if points >= 0.9:
            verdicts.append("Fantastic Day!")
        
        elif points >= 0.75:
            verdicts.append("Nice Work!")

        elif points >= 0.50:
            verdicts.append("Try Harder!")
        
        elif points >= 0.25:
            verdicts.append("Do Better!")
        
        else:
            verdicts.append("Are You Ok?")

    return render(request, "todoApp/progress.html", {
        "existing_days" : existing_days,
        "scores" : scores,
        "verdicts" : verdicts,
    })

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

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "todoApp/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "todoApp/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "todoApp/register.html")

