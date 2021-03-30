from django.urls import path
from .views import (
    AddItemView,
    CartView,
    RemoveItemView
)


app_name='shop'
urlpatterns = [
    path('shop/cart', CartView.as_view(), name='cart'),

    path('shop/add/item', AddItemView.as_view(), name='add_item'),
    path('shop/remove/item', RemoveItemView.as_view(), name='remove_item')
]
