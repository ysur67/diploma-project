from rest_framework import serializers
from apps.shop.models import Cart, CartItem
from apps.catalog.serializers import ProductDetailSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductDetailSerializer

    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    item = CartItemSerializer

    class Meta:
        model = Cart
        fields = '__all__'
