from urllib.parse import urlencode

from django import template

from goods.views import Categories
from django.utils.http import urlencode

register = template.Library()

@register.simple_tag()
def tag_categories():
    return Categories.objects.all().order_by("id")

@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)
