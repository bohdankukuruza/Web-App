from django.urls import path, URLPattern

from users import views

app_name = 'users'

urlpatterns: list[URLPattern] = [
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
]