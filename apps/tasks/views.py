from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authentication import TokenAuthentication
from django.contrib import messages
from .models import Task
from .serializer import TaskSerializer
from datetime import date, timedelta
from .forms import TaskForm, RegisterForm
from django.contrib.auth.models import User


# Create your views here.
# API views
class ApiTaskList(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

class ApiTaskDetail(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

# Server rendering logic
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)

    filter_status = request.GET.get("filter")
    allowed_sort = ["due_date", "created_at"]
    sort_by = request.GET.get("sort")
    today = date.today()
    soon_due_tasks = tasks.filter(
        due_date__lte=today + timedelta(days=2), completed=False
    )
    if soon_due_tasks.exists():
        messages.warning(request, "You have tasks due soon! ⏳")

    if filter_status == "completed":
        tasks = tasks.filter(completed=True)
    elif filter_status == "pending":
        tasks = tasks.filter(completed=False)

    if sort_by not in allowed_sort or sort_by == "default":
        tasks = tasks.order_by("completed", "due_date")
    else:
        tasks = tasks.order_by(sort_by)

    form = TaskForm()
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, "Task added successfully!")
            return redirect("task_list")
    return render(
        request,
        "tasks.html",
        {"tasks": tasks, "form": form, "user": request.user, "today": today},
    )


@login_required
def task_update(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user=request.user)
    except Task.DoesNotExist:
        return HttpResponseForbidden("You are not allowed to edit this task")

    form = TaskForm(instance=task)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully!")
            return redirect("task_list")
    return render(request, "task_update.html", {"form": form})


@login_required
def task_delete(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user=request.user)
    except Task.DoesNotExist:
        return HttpResponseForbidden("You are not allowed to delete this task")

    if request.method == "POST":
        task.delete()
        messages.success(request, "Task deleted successfully")
        return redirect("task_list")

    return render(request, "task_confirm_delete.html", {"task": task})


def register_view(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            if User.objects.filter(username=username).exists():
                messages.error(
                    request,
                    "Username already exists. Please choose a different username.",
                )
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
