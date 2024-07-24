from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, TaskForm
from .models import Task


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('task_list')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'task_list.html', {'tasks': tasks})


@login_required
def task_form(request, task_id=None):
    if task_id:
        task = get_object_or_404(Task, id=task_id, user=request.user)
    else:
        task = None

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'task_form.html', {'form': form, 'task': task})
