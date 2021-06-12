from django.contrib import admin
from .models import (
    Order, OrderItem,
    ShippingType, OrderStatus, PaymentType
)


class ItemInline(admin.TabularInline):
    model = OrderItem
    exclude = ('total', )
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display =('full_name', 'phone', 'email', 'date')
    # filter_horizontal = ''
    list_filter = ['date', 'shipping_type', 'order_status',]
    fieldsets = (
        (None, {
            "fields": (
                'user', 'full_name', 'phone', 
                'email', 'comment'
            ),
        }),
        ('Основная информация о заказе', {
            "fields": (
                'shipping_type', 'order_status', 
                'payment_type', 'total_price',
                'is_paid'
            )
        }),
        ('Информация о доставке', {
            'fields': (
                'city', 'street', 'building', 'appartment'
            )
        })
    )
    
    inlines = [ItemInline,]

@admin.register(ShippingType)
class ShippingAdmin(admin.ModelAdmin):
    pass

@admin.register(OrderStatus)
class StatusAdmin(admin.ModelAdmin):
    pass

@admin.register(PaymentType)
class StatusAdmin(admin.ModelAdmin):
    pass
