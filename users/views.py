from django.contrib.auth import login, logout, authenticate

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.shortcuts import render, redirect

from doc_analyze.models import Docs
from users.forms import RegistrationForm
from users.models import User


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # Перенаправляем на страницу входа
    else:
        form = RegistrationForm()
    return render(request, "users/register.html", {"form": form})


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)  # Проверяем данные
        if user is not None:
            login(request, user)  # Сохраняем пользователя в сессии
            return redirect("home")  # Перенаправляем на главную страницу
        else:
            return render(request, "users/login.html", {"error": "Неверные данные для входа"})
    return render(request, "users/login.html")


@login_required
def profile_view(request):
    # Проверка на правильность пользователя
    if not request.user.is_authenticated:
        return redirect('login')

    # Получаем все документы пользователя через промежуточную модель UsersToDocs
    user_docs = Docs.objects.filter(doc_users__user=request.user)

    return render(request, 'users/profile.html', {
        'user': request.user,
        'documents': user_docs
    })


@login_required
def logout_user(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('home')

@login_required
def profile(request):
    return render(request, 'users/profile.html', {'user': request.user})
