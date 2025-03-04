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
from apps.tasks.views import task_list, task_update, task_delete
from apps.tasks.views import ApiTaskDetail, ApiTaskList
from apps.tasks.views import register_view, login_view, logout_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # Login - Get access & refresh token
    TokenRefreshView,  # Refresh access token
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', task_list, name='task_list'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login endpoint
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token
    path('api/tasks/', ApiTaskList.as_view(), name='api_task_list'),
    path('api/tasks/<int:pk>/', ApiTaskDetail.as_view(), name='api_task_detail'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('<int:task_id>/update/', task_update, name='task_update'),
    path('<int:task_id>/delete/', task_delete, name='task_delete'),
]
