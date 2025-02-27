from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def task_list(request):
    return HttpResponse('<h1>Task List Page</h1>')

def task_detail(request):
    return HttpResponse('<h1>Task Details Page</h1>')