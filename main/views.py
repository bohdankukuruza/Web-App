from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    context: dict = {
        'title': 'Home',
        'content': 'The main page',
        'list': ['first', 'second', 'third'],
        'dict': {'first': 1},
        'bool': True,
        'is_authenticated': True,
    }
    return render(request, 'main/index.html', context)

def about(request):
    return HttpResponse("About Page")
