from django.http import HttpResponse
from django.shortcuts import render

from goods.models import Categories

def index(request):

    categories = Categories.objects.all()

    context: dict = {
        'title': 'Home - Главная',
        'content': 'Магазин мебели HOME',
        'categories': categories,
    }
    return render(request, 'main/index.html', context)

def about(request):
    context: dict = {
        'title': 'Home - О нас',
        'content': 'О нас',
        'text_on_page': 'екст тут asdasdasdasda',
    }
    return render(request, 'main/about.html', context)

