from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from apps.catalog.models import (
    Category,
    Product,
    AttributeValue,
    Attribute,
    FilterSet)
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.catalog.serializers import (
    CategoryListSerializer, 
    CategoryDetailSerializer,
    ProductListSerializer,
    AttributeValueSerializer,
    FitlerSetSerializer,
    )
from django.http import JsonResponse, HttpResponse
from rest_framework import (
    generics,
    permissions,
    viewsets
)
from django.db.models import Prefetch
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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        qs = Product.objects.filter(category=\
            Category.objects.get(slug=self.kwargs['slug']))
        context['category'] = Category.objects.get(
            slug=self.kwargs['slug']
        )
        if self.request.is_ajax():
            context['attributes'] = qs.attributes.all()
            return context
        else:
            return context

    def post(self, request, *args, **kwargs):
        category = Category.objects.get(slug=self.kwargs['slug'])
        if category.get_children()\
            or category.get_ancestors():
            qs = Product.objects.filter(
                category__in=category.get_family()
            ).prefetch_related('attributes')
        else:
            qs = Product.objects.filter(
                category=category
            ).prefetch_related('attributes')
        attributes_ids = []
        for product in qs:
            for option in product.attributes.all():
                attributes_ids.append(
                    option.attribute_value.attribute.id_1c
                )
        attributes = Attribute.objects.filter(
            id_1c__in=attributes_ids
        ).distinct('title').order_by('title')
        attribute_values = []
        for attribute in attributes:
            obj = FilterSet(attribute.title)
            for row in AttributeValue.objects.filter(attribute=attribute):
                obj.set_value(row)
            attribute_values.append(obj)
        serializer = FitlerSetSerializer(
            attribute_values,
            many=True
        )
        if request.is_ajax:
            return JsonResponse({'attributes':serializer.data})
        else:
            return JsonResponse({'log': None})

    def get_queryset(self, *args, **kwargs):
        obj = Category.objects.get(slug=self.kwargs['slug'])
        if self.has_children(obj):
            category_tree = obj.get_descendants(include_self=True)
            products = Product.objects.filter(category__in=category_tree)
        else:
            products = Product.objects.filter(category=obj)
        return products

    def has_children(self, instance):
        return True if len(instance.get_children()) >0 else False


class CategoryRestViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(parent=None)
    serializer_class = CategoryListSerializer
