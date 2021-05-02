from django.shortcuts import render
from django.views.generic import View
from apps.catalog.models import Product
from apps.shop.models import (
    Cart,
    CartItem,
    UnauthCart,
    UnauthCartItem,
    get_or_create_cart
)
from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.contrib.auth.models import User
from apps.shop.serializers import CartItemSerializer, CartSerializer, UnauthCartSerializer
from django.db.models import Sum


class AddItemView(View):
    
    def post(self, request, *args, **kwargs):
        user = self.request.user
        cart = get_or_create_cart(self.request)
        product_id = self.request.POST.get('productId')

        cart.set_product(product_id)
        # both of carts has same method 'count'
        # so it doesnt't matter which cart is given
        cart.count()

        if self.request.is_ajax():
            if not user.is_authenticated:
                serializer = UnauthCartSerializer(cart)
                self.request.session['cart'] = serializer.data
                self.request.session.modified = True
            return JsonResponse({
                'total': cart.total,
                'amount' : cart.amount,
                'message': 'Добавлен в корзину'
            })
        else:
            raise Http404('Такой страницы не существует!')



class RemoveItemView(View):
    
    def post(self, *args, **kwargs):
        user = self.request.user
        cart = get_or_create_cart(self.request)
        cart_item_id = self.request.POST.get('itemId')
        cart.remove_item(cart_item_id)
        # both of carts has same method 'count'
        # so it doesnt't matter which cart is given
        cart.count()

        if self.request.is_ajax():
            if not user.is_authenticated:
                serializer = UnauthCartSerializer(cart)
                self.request.session['cart'] = serializer.data
                self.request.session.modified = True
            return JsonResponse({
                'total': cart.total,
                'amount' : cart.amount,
                'message': 'Товар удален из корзины'
            })
        else:
            raise Http404('Такой страницы не существует!')



class CartView(View):
    model = Cart
    context_object_name = 'cart'
    template_name = 'shop/cart.html'

    def get(self, *args, **kwargs):
        cart = get_or_create_cart(self.request)
        return render(
            self.request,
            self.template_name,
            {'cart':cart}
        )
