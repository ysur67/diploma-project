from django.db import models
from apps.catalog.models import Product
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator


class Cart(models.Model):

    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='cart',
    )
    total = models.FloatField(
        validators=[MinValueValidator(0.0)],
        default=0,
    )

    def __str__(self):
        return str(self.user)
    


class CartItem(models.Model):
    cart = models.ForeignKey(
        'Cart',
        on_delete=models.CASCADE,
        related_name='items',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_items',
    )
    price = models.FloatField(
        validators=[MinValueValidator(0.0)],
        default=0,
    )
    amount = models.PositiveIntegerField(
        default=0,
    )
    total = models.FloatField(
        validators=[MinValueValidator(0.0)],
        default=0,
    )


    def __str__(self):
        return str(self.cart)
    

class UnauthCart:
    def __init__(self, user):
        self.user = user
        self.total = 0
        self.items = []    

    def get_items(self):
        return self.items

    def add_item(self, item):
        self.items.append(item)
    

class UnauthCartItem:
    def __init__(self, product, amount):
        self.product = product
        self.amount = amount
        self.total = product.price * amount
