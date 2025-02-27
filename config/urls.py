"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from apps.tasks.views import task_list, task_detail

def home(request):
    return HttpResponse('<h1>Welcome to TaskFlow</h1><p>TaskFlow is a simple task management system.</p>')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('tasks/', task_list),
    path('detail/', task_detail),
]
