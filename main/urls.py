from django.urls import path, URLPattern

from main import views

app_name = 'main'

urlpatterns: list[URLPattern] = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
]