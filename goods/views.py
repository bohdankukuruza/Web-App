from django.shortcuts import render

from goods.models import Product
from goods.models import Categories

def catalog(request):

    goods = Product.objects.all()

    context = {
        'title': 'Home Catalog',
        'goods': goods,
    }
    return render(request, 'goods/catalog.html', context)

def product(request):
    return render(request, 'goods/product.html')

