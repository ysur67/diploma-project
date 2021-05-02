from rest_framework import serializers
from apps.catalog.models import Category, Product, AttributeValue, ProductAttributeValue
from rest_framework import permissions


class RecuriveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class FilterCategorySerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)
        

class CategoryListSerializer(serializers.ModelSerializer):
    children = RecuriveSerializer(many=True)

    class Meta:
        # Using data.filter(**filters) isn't working with
        # rest_framework's pagination
        # serializer_class = FilterCategorySerializer
        model = Category
        exclude = ('rght', 'lft', 'tree_id', 'parent', 'level', 'image', 'description')


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField('title', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class CategoryDetailSerializer(serializers.ModelSerializer):
    children = RecuriveSerializer(many=True)

    class Meta:
        model = Category
        exclude = ('rght', 'lft', 'tree_id', 'parent', 'level')


class AttributeValueSerializer(serializers.ModelSerializer):

    attribute = serializers.SlugRelatedField('title', read_only=True)

    class Meta:
        model = AttributeValue
        fields = '__all__'

class ProductAttributeValueSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField('title', read_only=True)
    attribute = serializers.SlugRelatedField('title', read_only=True)

    class Meta:
        model = ProductAttributeValue
        fields = '__all__'


class FitlerSetSerializer(serializers.Serializer):
    title = serializers.CharField()
    values = AttributeValueSerializer(many=True)
