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
from apps.main.utils import OrderFormValidator, template_email_message
from django.urls import reverse_lazy, reverse
from apps.main.models import SiteSettings
from apps.shop.serializers import UnauthCartSerializer


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
        shippings = ShippingType.objects.filter(active=True).order_by('-id')
        shippings = shippings.filter(min_price__lt=cart.total)
        context['shippings'] = shippings
        context['payments'] = PaymentType.objects.filter(active=True).order_by('-id')
        return context

    def post(self, request, *args, **kwargs):
        post_data = request.POST.copy()
        request_addrress = post_data.get('address', None)
        json_response = {
            'errors': False,
            'fields': {},
            'message': ''
        }
        if request_addrress is None or request_addrress is "":
            json_response['errors'] = True
            json_response['fields'] = {'address': 'Заполните поле адреса'}
            return JsonResponse(json_response)

        suggestions = ShippingType.get_suggestions(request_addrress)
        return JsonResponse({'suggestions': suggestions})
    

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

        request_address = post_data.get('address')

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

        request_address = post_data.get('address')

        if shipping_type.is_calculated:
            shipping_price = shipping_type.calculate_shipping(request_address)
            if shipping_price < 1000:
                order.shipping_price = shipping_type.count_to_door_shipping(order.total_price)
            else:
                order.shipping_price = shipping_price
            order.full_address = request_address
        else:
            site_settings = SiteSettings.objects.first()
            order.full_address = site_settings.shop_address
        
        order.save()

        json_response['redirect'] = reverse('account:order_detail', args=[order.id])
        template_email_message(
            'shop/email.html', 'Спасибо за заказ',
            [post_data.get('email')], {'order': order, 'request': request}
        )
        cart.clear(request)
        if not user:
            serializer = UnauthCartSerializer(cart)
            self.request.session['cart'] = serializer.data
            self.request.session.modified = True

        return JsonResponse(json_response)


class CalculateShippingView(View):

    def post(self, request, *args, **kwargs):
        post_data = request.POST.copy()
        address = post_data.get('address')
        shipping_type = ShippingType.objects.get(id=post_data.get('shipping'))
        shipping_price = shipping_type.calculate_shipping(address)

        json_response = {'price': shipping_price}
        return JsonResponse(json_response)
