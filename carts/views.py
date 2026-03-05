from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from carts.models import Cart
from carts.utils import get_user_carts
from goods.models import Product
from carts.models import Cart
from django.urls import reverse

def render_cart_partials(request, context):
    modal_html = render_to_string(
        "carts/includes/included_cart_modal.html",
        context,
        request=request
    )
    page_html = render_to_string(
        "carts/includes/included_cart_page.html",
        context,
        request=request
    )
    return modal_html, page_html



def cart_add(request):

    product_id = request.POST.get("product_id")
    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)

    else:
        carts = Cart.objects.filter(
            session_key=request.session.session_key, product=product)

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(session_key=request.session.session_key, product=product, quantity=1)

    user_cart = get_user_carts(request)
    context = {"carts": user_cart}
    modal_html, page_html = render_cart_partials(request, context)

    response_data = {
        "message": "Товар добавлен в корзину",
        "cart_items_html_modal": modal_html,
        "cart_items_html_page": page_html,
        "cart_total_quantity": user_cart.total_quantity,
    }
    return JsonResponse(response_data)

def cart_change(request):
    cart_id = request.POST.get("cart_id")
    quantity = request.POST.get("quantity")

    cart = Cart.objects.get(id=cart_id)

    cart.quantity = quantity
    cart.save()

    user_cart = get_user_carts(request)

    context = {"carts": user_cart}

    # if referer page is create_order add key orders: True to context
    referer = request.META.get("HTTP_REFERER") or ""
    if reverse("orders:create_order") in referer:
        context["order"] = True

    modal_html, page_html = render_cart_partials(request, context)

    response_data = {
        "message": "Количество изменено",
        "cart_items_html_modal": modal_html,
        "cart_items_html_page": page_html,
        "quantity": quantity,
        "cart_total_quantity": user_cart.total_quantity,
    }

    return JsonResponse(response_data)

def cart_remove(request):

    cart_id = request.POST.get("cart_id")
    cart = Cart.objects.get(id=cart_id)
    quantity = cart.quantity
    cart.delete()

    user_cart = get_user_carts(request)

    context = {"carts": user_cart}

    # if referer page is create_order add key orders: True to context
    referer = request.META.get("HTTP_REFERER") or ""
    if reverse("orders:create_order") in referer:
        context["order"] = True

    modal_html, page_html = render_cart_partials(request, context)

    response_data = {
        "message": "Товар удален",
        "cart_items_html_modal": modal_html,
        "cart_items_html_page": page_html,
        "quantity_deleted": quantity,
        "cart_total_quantity": user_cart.total_quantity,
    }

    return JsonResponse(response_data)