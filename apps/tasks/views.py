from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from .models import Task
from .forms import TaskForm, RegisterForm
from django.contrib.auth.models import User


# Create your views here.
@login_required
def task_list(request):
    tasks = Task.objects.all().order_by("completed", "due_date")
    form = TaskForm()
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Task added successfully!")
            return redirect("task_list")
    return render(request, "tasks.html", {"tasks": tasks, "form": form})


def task_detail(request):
    return HttpResponse("<h1>Task Details Page</h1>")


def register_view(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists. Please choose a different username.")
            else:
                user = form.save(commit=False)
                password = form.cleaned_data.get("password")
                user.set_password(password)
                user.save()
                messages.success(request, "Account created successfully!")
                login(request, user)
                return redirect("task_list")
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        redirect(task_list)
        
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("task_list")
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")
