from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from apps.catalog.models import (
    Category,
    Product,
    AttributeValue,
    Attribute,
    FilterSet,
    ProductAttributeValue
)
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.catalog.serializers import (
    CategoryListSerializer, 
    CategoryDetailSerializer,
    ProductListSerializer,
    ProductAttributeValueSerializer,
    AttributeValueSerializer,
    FitlerSetSerializer,
)
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from rest_framework import (
    generics,
    permissions,
    viewsets
)
from rest_framework.decorators import action
from django.db.models import Prefetch, Q
from itertools import chain


class CatalogView(ListView):
    model = Category
    template_name = 'catalog/catalog.html'

    def get_queryset(self, *args, **kwargs):
        return Category.objects.filter(active=True, parent=None)




class CategoryJSONDetail(ListView):
    model = Category
    context_object_name = 'product_list'
    template_name = 'catalog/product_list.html'
    paginate_by = 10

    def get(self, *args, **kwargs):
        request = self.request.GET
        if request.getlist('value'):
            values_list = request.getlist('value')
            self.object_list = self.get_queryset()
            qs = self.object_list
            context = self.get_context_data()
            qs = qs.filter(
                attributes__attribute_value__id__in=values_list
            )
            context['product_list'] = qs
            return render(
                self.request,
                self.template_name,
                context=context
            )
        else:
            return super().get(self.request)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        qs = self.get_queryset()
        context['category'] = Category.objects.get(
            slug=self.kwargs['slug']
        )
        context['attribute_list'] = self.get_filter_set(qs)
        context['count'] = qs.count()
        return context

    def get_queryset(self, *args, **kwargs):
        obj = Category.objects.get(slug=self.kwargs['slug'])
        if self.has_children(obj):
            category_tree = obj.get_descendants(include_self=True)
            products = Product.objects.filter(category__in=category_tree)
        else:
            products = Product.objects.filter(category=obj)
        return products

    def get_filter_set(self, qs):
        # Получаем все Товар-Атрибут-Значения исходя из товаров в запросе
        product_attribute_value = ProductAttributeValue.objects.filter(
            product__in=qs
        )
        # Получаем все Атрибут-Значения исходя из полученных выше
        attribute_values = AttributeValue.objects.filter(
            products__in=product_attribute_value
        ).distinct('value')
        # Получаем все названия атрибутов
        titles = attribute_values.distinct('attribute')
        # Пытаемся создать словарь ТайтлАтрибута = [Значения атрибута]
        filter_list = []
        for attribute_value in titles:
            filter_ = FilterSet(attribute_value.attribute.title)
            for value in attribute_values.filter(attribute=attribute_value.attribute):
                filter_.set_value(value)
            filter_list.append(filter_)
        serializer = FitlerSetSerializer(filter_list, many=True)
        return serializer.data

    def has_children(self, instance):
        return True if len(instance.get_children()) >0 else False
