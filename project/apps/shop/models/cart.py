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
    amount = models.PositiveIntegerField(
        default=0,
    )

    def __str__(self):
        return str(self.user)

    def get_items(self):
        return self.items.all()

    def count(self):
        total_price = 0.0
        count_price = lambda item: item.product.price * item.amount
        total_price = [count_price(item) for item in self.items.all()]
        total_price = float(sum(total_price))
        self.total = total_price
        self.amount = 0
        for item in self.items.all():
            self.amount += item.amount
        self.save()

    def set_product(self, product_id, product_amount=None):
        product = Product.objects.get(id=product_id)
        cart_item = self.items.filter(product=product)
        amount = product_amount if product_amount else 1
        if cart_item.exists():
            item = CartItem.objects.get(cart=self, product=product)
            item.amount += amount
            if item.amount > product.amount:
                item.amount = product.amount
            item.total = item.amount * item.product.price
            item.save()
        elif not cart_item.exists():
            amount = product_amount if product_amount else 1
            CartItem.objects.create(
                cart=self, product=product,
                amount=amount,
                total=product.price * amount 
            )
        self.save()

    def clear(self, _):
        self.items.all().delete()
        self.total = 0
        self.amount = 0
        self.save()

    def remove_item(self, item_id):
        product = Product.objects.get(
            id=item_id
        )
        CartItem.objects.get(
            cart=self,
            product=product
        ).delete()


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
    def __init__(self, user, total=None, items=None):
        self.user = user
        if total:
            self.total = total
        else:
            self.total = 0
        if items:
            self.items = items
        else:
            self.items = []
        self.amount = 0

    def get_items(self):
        return self.items

    def add_item(self, item):
        self.items.append(item)

    def count(self):
        total_price = 0.0
        count_price = lambda item: item.product.price * item.amount
        total_price = [count_price(item) for item in self.get_items()]
        total_price = float(sum(total_price))
        self.amount = 0
        for item in self.items:
            self.amount += item.amount
        self.total = total_price

    def set_product(self, product_id, product_amount):
        product = Product.objects.get(id=product_id)
        item = UnauthCartItem(product, product_amount)
        item_in_cart = False
        for cart_item in self.items:
            if item.product == cart_item.product:
                cart_item.amount += product_amount if product_amount else 1
                cart_item.count()
                self.count()
                item_in_cart = True
        if item_in_cart is False:
            self.add_item(item)

    def remove_item(self, item_id):
        product = Product.objects.get(
            id=item_id
        )
        item = UnauthCartItem(product, 1)
        for index, cart_item in enumerate(self.items):
            if item.product == cart_item.product:
                self.items.pop(index)

    def clear(self, request):
        self.items.clear()
        self.count()


class UnauthCartItem:
    def __init__(self, product, amount):
        self.product = product
        self.amount = amount
        self.total = product.price * amount

    def count(self):
        self.total = self.product.price * self.amount


def get_or_create_cart(request):
    # TODO: В будущем поправить
    user = request.user
    if user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=user)
    else:
        if request.session.get('cart', None):
            cart = request.session.get('cart')
            items = {}
            for item in cart.get('items'):
                product_id = item.get('product').get('id')
                product = Product.objects.get(id=product_id)
                items[product] = item.get('amount')
            items = [UnauthCartItem(key, items.get(key)) for key in items]
            cart = UnauthCart(
                user=cart.get('user'),
                total=cart.get('total'),
                items=items
            )

        else:
            cart = UnauthCart(user)
    return cart
