from django.shortcuts import render
from django.views.generic.base import TemplateView
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
        if not request.is_ajax():
            raise Http404('Такой страницы не существует!')

        user = self.request.user
        post_data = request.POST.copy()
        cart = get_or_create_cart(self.request)
        product_id = post_data.get('productId')
        amount = post_data.get('amount', 1)
        amount = int(amount)
        json_reponse = {
            'errors': False,
            'fields': {},
            'total': None,
            'amount': None,
            'message': ''
        }
        product = Product.objects.get(id=int(product_id))
        if product.amount < amount:
            json_reponse['errors'] = True
            json_reponse['fields']['amount'] = "Такого количества нет на складе"
            return JsonResponse(json_reponse)

        cart.set_product(product_id, amount)
        # both of carts has same method 'count'
        # so it doesnt't matter which cart is given
        cart.count()

        if not user.is_authenticated:
            serializer = UnauthCartSerializer(cart)
            self.request.session['cart'] = serializer.data
            self.request.session.modified = True

        json_reponse['total'] = cart.total
        json_reponse['amount'] = cart.amount
        json_reponse['message'] = 'Добавлен в корзину'
        return JsonResponse(json_reponse)



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



class CartView(TemplateView):
    model = Cart
    context_object_name = 'cart'
    template_name = 'shop/cart.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['cart'] = get_or_create_cart(self.request)
        return context
