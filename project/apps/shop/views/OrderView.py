from apps.shop.models import (
    Cart,
    Order,
    OrderItem,
    get_or_create_cart,
    ShippingType,
    PaymentType,
    OrderStatus
)
from django.shortcuts import redirect as django_redirect
from django.views.generic import View, TemplateView
from django.http import JsonResponse
from apps.main.utils import OrderFormValidator
from django.urls import reverse_lazy
from apps.main.utils import template_email_message


class RegisterOrder(TemplateView):
    template_name = 'shop/register_order.html'

    def render_to_response(self, context, **response_kwargs):
        cart = get_or_create_cart(self.request)
        items = cart.get_items()
        if not cart or not items:
            return django_redirect('/')
        return super().render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_or_create_cart(self.request)
        context['cart'] = cart
        context['shippings'] = ShippingType.objects.filter(active=True)
        context['payments'] = PaymentType.objects.filter(active=True)
        return context
    

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
        json_response = {
            'errors': False,
            'fields': {},
            'message': ''
        }

        post_data = data.copy()
        validator = OrderFormValidator(post_data)
        if validator.has_errors:
            json_response['errors'] = True
            json_response['fields'] = validator.errors
            return JsonResponse(json_response)

        order = Order.objects.create(
            user=user,
            full_name=post_data.get('full_name'),
            phone=post_data.get('phone'),
            email=post_data.get('email'),
            shipping_type=shipping_type,
            order_status=OrderStatus.objects.get(id='WIP'),
            payment_type=payment_type,
            city=post_data.get('city'),
            street=post_data.get('street'),
            building=post_data.get('building'),
            total_price=cart.total,
            comment=post_data.get('comment')
        )
        items = cart.get_items()
        if not items:
            json_response['redirect'] = reverse_lazy('shop:cart')
            return JsonResponse(json_response)

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                amount=item.amount,
                product_price=item.product.price,
                total=item.total
            )
        json_response['redirect'] = reverse_lazy('index_page')
        template_email_message(
            'shop/email.html', 'Спасибо за заказ',
            [post_data.get('email')], {'order': order, 'request': request}
        )
        cart.clear(request)
        return JsonResponse(json_response)
