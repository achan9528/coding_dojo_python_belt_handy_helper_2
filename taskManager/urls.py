from . import views
from django.urls import path

app_name = "taskManager"

urlpatterns = [
    path('', views.index, name="index"),
    path('register', views.register, name="register"),
    path('login', views.login, name="login"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('jobs/new', views.newJobForm, name="newJobForm"),
    path('jobs/new/add', views.addJob, name="addJob"),
    path('jobs/view/<int:taskID>', views.viewTask, name="viewTask"),
    path('jobs/remove/<int:taskID>', views.removeTaskForm, name="removeTaskForm"),
    path('jobs/remove/<int:taskID>/remove', views.removeTask, name="removeTask"),
    path('jobs/edit/<int:taskID>', views.editTaskForm, name="editTaskForm"),
    path('jobs/edit/<int:taskID>/edit', views.editTask, name="editTask"),
    path('jobs/claim/<int:taskID>', views.claimTask, name="claimTask"),
    path('jobs/complete/<int:taskID>', views.completeTask, name="completeTask"),
    path('jobs/release/<int:taskID>', views.releaseTask, name="releaseTask"),
    path('logout', views.logout, name="logout"),
]