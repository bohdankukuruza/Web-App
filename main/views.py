from django.http import HttpResponse
from django.shortcuts import render

from goods.models import Categories

def index(request):

    context: dict = {
        'title': 'Home - Главная',
        'content': 'Магазин мебели HOME',
    }
    return render(request, 'main/index.html', context)

def about(request):
    context: dict = {
        'title': 'Home - О нас',
        'content': 'О нас',
        'text_on_page': 'екст тут asdasdasdasda',
    }
    return render(request, 'main/about.html', context)

def delivery(request):
    context: dict = {
        'title': 'Delivery',
    }
    return render(request, 'main/delivery.html', context)

def contact(request):
    context: dict = {
        'title': 'Contact',
    }
    return render(request, 'main/contact.html', context)

