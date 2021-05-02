from django.urls import path
from .views import (
    AddItemView,
    CartView,
    RemoveItemView,
    RegisterOrder,
    CreateOrder
)


app_name='shop'
urlpatterns = [
    path('shop/cart', CartView.as_view(), name='cart'),
    path('shop/order', RegisterOrder.as_view(), name='order_register'),

    path('shop/order/create', CreateOrder.as_view(), name='order_create'),

    path('shop/add/item', AddItemView.as_view(), name='add_item'),
    path('shop/remove/item', RemoveItemView.as_view(), name='remove_item')
]
