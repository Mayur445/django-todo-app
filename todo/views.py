from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Task


# 🏠 Public Home Page (before login)
def home(request):
    if request.user.is_authenticated:
        return redirect('index')  # If already logged in → go to tasks
    return render(request, 'todo/home.html')


# 📋 Dashboard — Shows logged-in user’s tasks
@login_required(login_url='login')
def index(request):
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'todo/index.html', {'tasks': tasks})


# ➕ Add a new task
@login_required(login_url='login')
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()

        if not title:
            messages.error(request, "Task title cannot be empty.")
        else:
            Task.objects.create(user=request.user, title=title, description=description)
            messages.success(request, "✅ Task added successfully!")

        return redirect('index')

    return render(request, 'todo/add_task.html')


# 🔄 Toggle completion status
@login_required(login_url='login')
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = not task.completed
    task.save()
    if task.completed:
        messages.success(request, f"🎉 '{task.title}' marked as completed.")
    else:
        messages.info(request, f"'{task.title}' marked as incomplete.")
    return redirect('index')


# ❌ Delete a task
@login_required(login_url='login')
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    messages.success(request, "🗑 Task deleted successfully.")
    return redirect('index')


# 🧑‍💻 Register a new user
def register_user(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')

        if not username or not password or not confirm:
            messages.error(request, "⚠️ All fields are required.")
            return redirect('register')

        if password != confirm:
            messages.error(request, "❌ Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "⚠️ Username already exists.")
            return redirect('register')

        User.objects.create_user(username=username, password=password)
        messages.success(request, "✅ Account created successfully! Please log in.")
        return redirect('login')

    return render(request, 'todo/register.html')


# 🔐 Login user
def login_user(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"👋 Welcome back, {username}!")
            return redirect('index')
        else:
            messages.error(request, "❌ Invalid username or password.")
            return redirect('login')

    return render(request, 'todo/login.html')


# 🚪 Logout user
@login_required(login_url='login')
def logout_user(request):
    logout(request)
    messages.success(request, "👋 You’ve been logged out successfully.")
    return redirect('login')
