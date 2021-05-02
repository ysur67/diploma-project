from apps.shop.models import (
    Cart,
    Order,
    OrderItem,
    get_or_create_cart,
    ShippingType,
    PaymentType,
    OrderStatus
)
from django.views.generic import View, TemplateView
from django.shortcuts import render
from django.http import JsonResponse


class RegisterOrder(TemplateView):
    template_name = 'shop/register_order.html'
    
    def get(self, *args, **kwargs):
        cart = get_or_create_cart(self.request)
        context = {
            'cart': cart,
            'shippings': ShippingType.objects.filter(active=True),
            'payments': PaymentType.objects.filter(active=True)
        }
        return render(
            self.request,
            self.template_name,
            context=context
        )

class CreateOrder(View):
    
    def post(self, *args, **kwargs):
        request = self.request
        user = self.request.user
        data = request.POST
        cart = get_or_create_cart(self.request)
        user = user if request.user.is_authenticated else None
        shipping_type = ShippingType.objects.get(
            id=data.get('shipping')
        )
        payment_type = PaymentType.objects.get(
            id=data.get('payment')
        )
        order = Order.objects.create(
            user=user,
            full_name=data.get('username'),
            phone=data.get('phone'),
            email=data.get('email'),
            shipping_type=shipping_type,
            order_status=OrderStatus.objects.get(id='WIP'),
            payment_type=payment_type,
            city=data.get('city'),
            street=data.get('street'),
            building=data.get('building'),
            total_price=cart.total,
            comment=data.get('comment')
        )
        items = cart.get_items()
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                amount=item.amount,
                product_price=item.product.price,
                total=item.total
            )
        return JsonResponse({
            'redirect': '/catalog/'
        })
