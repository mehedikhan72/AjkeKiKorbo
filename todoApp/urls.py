from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout" , views.logout_view, name="logout"),
    path("today's-tasks", views.today, name="today"),
    path("add_task/<str:day>", views.add_task, name="add_task"),
    path("complete_task/<int:id>", views.complete_task, name="complete_task"),
    path("delete_task/<int:id>/<str:day>", views.delete_task, name="delete_task"),
    path("tomorrow's-tasks", views.tomorrow, name="tomorrow"),
    path("progress", views.progress, name="progress")
]
