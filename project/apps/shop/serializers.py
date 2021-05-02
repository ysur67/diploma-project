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


class UnauthCartItemSerializer(serializers.Serializer):
    product = ProductDetailSerializer()
    amount = serializers.IntegerField()
    total = serializers.FloatField()

class UnauthCartSerializer(serializers.Serializer):
    items = serializers.ListField(
        child = UnauthCartItemSerializer()
    )
    total = serializers.FloatField()
    amount = serializers.IntegerField()
    # integers = serializers.ListField(
    # child = serializers.IntegerField(min_value = 0, max_value = 100)
    # )
