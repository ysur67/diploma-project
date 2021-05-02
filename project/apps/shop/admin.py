from django.contrib import admin
from .models import (
    Order, OrderItem,
    ShippingType, OrderStatus, PaymentType
)


class ItemInline(admin.TabularInline):
    model = OrderItem
    exclude = ('total', )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
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
