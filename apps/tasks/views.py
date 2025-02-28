from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Task
from .forms import TaskForm

# Create your views here.
def task_list(request):
    tasks = Task.objects.all().order_by('completed', 'due_date')
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task added successfully!')
            return redirect('task_list')
    return render(request, 'tasks.html', {'tasks': tasks, 'form': form})

def task_detail(request):
    return HttpResponse('<h1>Task Details Page</h1>')