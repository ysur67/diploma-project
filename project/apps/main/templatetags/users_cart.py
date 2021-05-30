from django import template
from apps.shop.models import Cart

register = template.Library()

@register.simple_tag(takes_context=False,
    name='count_cart')
def count_cart(request):
    # TODO: make it prettier
    user = request.user if request.user.is_authenticated else None
    if user:  
        if Cart.objects.filter(user=user).exists():
            cart = Cart.objects.get(user=user)
            if cart.total == 0.0:
                return "Корзина"
            else:
                return str(cart.total) + " ₽"
        else:
            return "Корзина"
    else:
        cart = request.session.get('cart', None)
        if cart:
            if cart.get('total') == 0.0:
                return "Корзина"
            else:
                return str(cart.get('total')) + " ₽"
        else:
            return "Корзина"


@register.simple_tag(takes_context=True)
def cart_amount(context):
    request = context.get("request")
    user = request.user if request.user.is_authenticated else None
    if user:  
        if Cart.objects.filter(user=user).exists():
            cart = Cart.objects.get(user=user)
            if cart.amount < 1:
                return None
            else:
                return str(cart.amount)
        else:
            return None
    else:
        cart = request.session.get('cart', None)
        if cart:
            if cart.get('amount') < 1:
                return None
            else:
                return str(cart.get('amount'))
        else:
            return None
