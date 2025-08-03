from django.db import models
from goods.models import Product
from users.models import User

class CartQuerySet(models.QuerySet):

    def total_price(self):
        return sum(cart.products_price() for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0

class Cart(models.Model):

    user = models.ForeignKey(to=User, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name='Продукт')
    quantity = models.PositiveSmallIntegerField(default=0.0, verbose_name='Количество')
    session_key = models.CharField(blank=True, null=True, max_length=40)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        db_table = 'cart'
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'

    objects = CartQuerySet.as_manager()

    def products_price(self):
        return round(self.product.sell_price() * self.quantity, 2)

    def __str__(self):
        return f"Корзина {self.user.username} | Товар {self.product.name} | Количество {self.quantity}"
