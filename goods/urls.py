from django.urls import path, URLPattern

from goods import views

app_name = 'catalog'

urlpatterns: list[URLPattern] = [
    path('search/', views.catalog, name='search'),
    path('<slug:category_slug>/', views.catalog, name='index'),
    path('product/<slug:product_slug>/', views.product, name='product'),
]