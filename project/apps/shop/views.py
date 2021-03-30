from django.shortcuts import render
from django.views.generic import View
from apps.catalog.models import Product
from apps.shop.models import (
    Cart,
    CartItem,
    UnauthCart,
    UnauthCartItem,
)
from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.contrib.auth.models import User
from apps.shop.serializers import CartItemSerializer, CartSerializer
from django.db.models import Sum


class AddItemView(View):
    
    def post(self, request, *args, **kwargs):
        user = self.request.user
        cart = get_or_create_cart(user, request=self.request)
        product_id = self.request.POST.get('productId')
        if user.is_authenticated:
            set_cart_items(cart, product_id)
        else:
            set_unauth_cart_items(cart, product_id, self.request)

        if user.is_authenticated:
            count_cart(cart)
        else:
            count_unauth_cart(cart, self.request)

        if self.request.is_ajax():
            serializer = CartSerializer(cart)
            self.request.session['cart'] = serializer.data
            return JsonResponse({
                'total': cart.total,
                'message': 'Добавлен в корзину'
            })
        else:
            raise Http404('Такой страницы не существует!')



class RemoveItemView(View):
    
    def post(self, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated:
            cart = get_or_create_cart(user)
        cart_item_id = self.request.POST.get('itemId')
        remove_item_from_cart(cart, cart_item_id)
        if user.is_authenticated:
            count_cart(cart)
        else:
            count_unauth_cart(cart, self.request)

        if self.request.is_ajax():
            serializer = CartSerializer(cart)
            self.request.session['cart'] = serializer.data
            return JsonResponse({
                'total': cart.total,
                'message': 'Товар удален из корзины'
            })
        else:
            raise Http404('Такой страницы не существует!')



class CartView(View):
    model = Cart
    context_object_name = 'cart'
    template_name = 'shop/cart.html'

    def get(self, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated:
            cart = user.cart
        else:
            cart = self.request.session['cart']
        return render(
            self.request,
            self.template_name,
            {'cart':cart}
        )


def get_or_create_cart(user, request=None):
    if user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=user)
    else:
        cart = UnauthCart(user)
        if request:
            request.session['cart'] = cart
    return cart

def set_cart_items(cart, product_id):
    product = Product.objects.get(id=product_id)
    if CartItem.objects.filter(cart=cart, product=product).exists():
        item = CartItem.objects.get(
            cart=cart,
            product=product,
        )
        item.amount = item.amount + 1
        item.total = item.amount * item.price
        item.save()
    else:
        CartItem.objects.create(
            cart=cart,
            product=product,
            price=product.price,
            amount=1,
            total=product.price*1,
        )

def set_unauth_cart_items(cart, product_id, request):
    product = Product.objects.get(id=product_id)
    cart = request.session['cart']
    item = UnauthCartItem(product, 1)
    if cart:
        cart.add_item(item)
        request.session['cart'] = cart
    else:
        cart = get_or_create_cart(request.user)
        cart.add_item(item)
        request.session['cart'] = cart

def count_cart(cart):
    total_price = 0.0
    count_price = lambda item: item.price * item.amount
    total_price = [count_price(item) for item in CartItem.objects.filter(cart=cart)]
    total_price = float(sum(total_price))
    cart.total = total_price
    cart.save()

def count_unauth_cart(cart, request):
    total_price = 0.0
    count_price = lambda item: item.product.price * item.amount
    total_price = [count_price(item) for item in cart.get_items()]
    total_price = float(sum(total_price))
    cart.total = total_price
    request.session['cart'] = cart

def remove_item_from_cart(cart, item_id):
    CartItem.objects.get(id=item_id).delete()
