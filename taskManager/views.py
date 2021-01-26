from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Task, Category
import bcrypt

# Create your views here.
def index(request):
    return render(request, "loginPage.html")

def login(request):
    errors = User.objects.loginValidator(request.POST)
    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request, value)
        return redirect("taskManager:index")
    else:
        loggedUser = User.objects.filter(email=request.POST["email"])[0]
        if bcrypt.checkpw(request.POST['password'].encode(), loggedUser.password.encode()):
            request.session["userID"] = loggedUser.id
            return redirect("taskManager:dashboard")
        else:
            messages.error(request, "Incorrect password - please try again!")
            return redirect("taskManager:index")

def register(request):
    errors = User.objects.registrationValidator(request.POST)
    if len(errors)>0:
        for key,value in errors.items():
            messages.error(request,value)
        return redirect("taskManager:index")
    else:
        password = request.POST['password']
        pwHash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        newUser = User.objects.create(
            firstName = request.POST['firstName'],
            lastName = request.POST['lastName'],
            email = request.POST['email'],
            password = pwHash
        )
        request.session['userID'] = newUser.id
        messages.success(request, "Thanks for joining us!")
        return redirect("taskManager:dashboard")

def dashboard(request):
    if 'userID' not in request.session:
        messages.error(request, "Please log in or register first!")
        return redirect('taskManager:index')
    loggedUser = User.objects.get(id=request.session['userID'])
    context = {
        "loggedUser" : loggedUser,
        "tasks": Task.objects.order_by("-createdAt"),
    }
    return render(request, "dashboard.html", context)

def newJobForm(request):
    if 'userID' not in request.session:
        messages.error(request, "Please log in or register first!")
        return redirect('taskManager:index')
    loggedUser = User.objects.get(id=request.session['userID'])
    context = {
        "loggedUser":loggedUser,
        "categories":Category.objects.all(),
    }
    return render(request, "newJobForm.html", context)

def addJob(request):
    if 'userID' not in request.session:
        messages.error(request, "Please log in or register first!")
        return redirect('taskManager:index')
    errors = Task.objects.inputValidator(request.POST)
    errors2 = Category.objects.inputValidator(request.POST)
    if len(errors)>0 or len(errors2)>0:
        for key,value in errors.items():
            messages.error(request,value)
        for key,value in errors2.items():
            messages.error(request,value)
        return redirect("taskManager:newJobForm")
    else:
        newTask = Task.objects.create(
            title = request.POST['title'],
            desc = request.POST['desc'],
            location = request.POST['location'],
            addedBy = User.objects.get(id=request.session['userID']),
        )

        for cat in Category.objects.all():
            if cat.title in request.POST:
                newTask.categories.add(Category.objects.get(title=cat.title))
        if request.POST['categoryOther'] != "":
            newCat = Category.objects.create(
                title=request.POST['categoryOther']
            )
            newTask.categories.add(newCat)

        messages.success(request, f"Task \"{newTask.title}\" Added!")
        return redirect("taskManager:dashboard")

def viewTask(request, taskID):
    if 'userID' not in request.session:
        messages.error(request, "Please log in or register first!")
        return redirect('taskManager:index')
    loggedUser = User.objects.get(id=request.session['userID'])
    context = {
        "loggedUser":loggedUser,
        "task": Task.objects.get(id=taskID),
    }
    return render(request, "viewJob.html", context)

def removeTaskForm(request, taskID):
    if 'userID' not in request.session:
        messages.error(request, "Please log in or register first!")
        return redirect('taskManager:index')
    loggedUser = User.objects.get(id=request.session['userID'])
    context = {
        "loggedUser":loggedUser,
        "task": Task.objects.get(id=taskID),
    }
    return render(request, "removeJobForm.html", context)

def removeTask(request, taskID):
    if 'userID' not in request.session:
        messages.error(request, "Please log in or register first!")
        return redirect('taskManager:index')
    taskToBeDeleted = Task.objects.get(id=taskID)
    title = taskToBeDeleted.title
    taskToBeDeleted.delete()
    messages.success(request, f"Task \"{title}\" deleted!")
    return redirect("taskManager:dashboard")

def editTaskForm(request, taskID):
    if 'userID' not in request.session:
        messages.error(request, "Please log in or register first!")
        return redirect('taskManager:index')
    loggedUser = User.objects.get(id=request.session['userID'])
    context = {
        "loggedUser":loggedUser,
        "task": Task.objects.get(id=taskID),
        "categories": Category.objects.all(),
    }
    return render(request,"editJobForm.html", context)

def editTask(request, taskID):
    if 'userID' not in request.session:
        messages.error(request, "Please log in or register first!")
        return redirect('taskManager:index')
    errors = Task.objects.inputValidator(request.POST)
    errors2 = Category.objects.inputValidator(request.POST)
    if len(errors)>0 or len(errors2):
        for key,value in errors.items():
            messages.error(request,value)
        for key,value in errors2.items():
            messages.error(request,value)
        return redirect("taskManager:editTaskForm", taskID=taskID)
    else:
        currentTask = Task.objects.get(id=taskID)
        currentTask.title = request.POST['title']
        currentTask.desc = request.POST['desc']
        currentTask.location = request.POST['location']

        for cat in Category.objects.all():
            if cat.title in request.POST:
                currentTask.categories.add(Category.objects.get(title=cat.title))
            else:
                currentTask.categories.remove(Category.objects.get(title=cat.title))
        if request.POST['categoryOther'] != "":
            newCat = Category.objects.create(
                title=request.POST['categoryOther']
            )
            currentTask.categories.add(newCat)

        currentTask.save()
        messages.success(request, f"Task \"{currentTask.title}\" modified!")
        return redirect("taskManager:dashboard")

def claimTask(request, taskID):
    if 'userID' not in request.session:
        messages.error(request, "Please log in or register first!")
        return redirect('taskManager:index')
    currentTask = Task.objects.get(id=taskID)
    loggedUser = User.objects.get(id=request.session['userID'])
    currentTask.owner = loggedUser
    currentTask.save()
    messages.success(request, f"Task \"{currentTask.title}\" claimed!")
    return redirect("taskManager:dashboard")

def completeTask(request, taskID):
    if 'userID' not in request.session:
        messages.error(request, "Please log in or register first!")
        return redirect('taskManager:index')
    currentTask = Task.objects.get(id=taskID)
    loggedUser = User.objects.get(id=request.session['userID'])
    currentTask.delete()
    # currentTask.isComplete = True
    # currentTask.save()
    messages.success(request, f"Task \"{currentTask.title}\" completed!")
    return redirect("taskManager:dashboard")

def releaseTask(request, taskID):
    if 'userID' not in request.session:
        messages.error(request, "Please log in or register first!")
        return redirect('taskManager:index')
    currentTask = Task.objects.get(id=taskID)
    loggedUser = User.objects.get(id=request.session['userID'])
    currentTask.owner = None
    # currentTask.isComplete = True
    # currentTask.save()
    currentTask.save()
    messages.success(request, f"Task \"{currentTask.title}\" released!")
    return redirect("taskManager:dashboard")

def logout(request):
    request.session.clear()
    messages.success(request, "Successfully Logged Out")
    return redirect("taskManager:index")