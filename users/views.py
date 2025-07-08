from django.shortcuts import render

def login(request):
    context = {
        'title': 'Home - Авторизация'
    }
    return render(request, "users/login.html", context)

def registration(request):
    context = {
        'title': 'Home - Регистарция'
    }
    return render(request, "users/registration.html", context)

def profile(request):
    context = {
        'title': 'Home - Кабинет'
    }
    return render(request, "users/profile.html", context)

def logout(request):
    context = {
        'title': 'Home'
    }
    return render(request, "users/logout.html", context)