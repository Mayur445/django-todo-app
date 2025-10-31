from django.urls import path
from . import views
from django.shortcuts import render

urlpatterns = [
    # 🏠 Home page (accessible without login)
    path('', lambda request: render(request, 'todo/home.html'), name='home'),

    # 📋 Task-related URLs
    path('tasks/', views.index, name='index'),
    path('add/', views.add_task, name='add_task'),
    path('update/<int:task_id>/', views.update_task, name='update_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),

    # 👤 Authentication URLs
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]
