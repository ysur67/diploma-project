from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from apps.catalog.models import Category, Product
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.catalog.serializers import (
    CategoryListSerializer, 
    CategoryDetailSerializer
    )
from django.http import JsonResponse, HttpResponse
from rest_framework import generics, permissions
from rest_framework import generics, viewsets


class CatalogView(ListView):
    model = Category
    template_name = 'catalog/catalog.html'

    def get_queryset(self, *args, **kwargs):
        return Category.objects.filter(active=True, parent=None)


class CategoryJSONDetail(ListView):
    model = Category
    context_object_name = 'product-category'
    template_name = 'catalog/product_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        qs = Product.objects.filter(category=\
            Category.objects.get(slug=self.kwargs['slug']))
        if self.request.is_ajax():
            context['attributes'] = qs.attributes.all()
            return context
        else:
            return context
            
    def post(self, request, *args, **kwargs):
        qs = Product.objects.filter(category=\
            Category.objects.get(slug=self.kwargs['slug']))

        attributes = qs.get_attributes()
        

        if request.is_ajax:
            return JsonResponse({'attributes':'still None'})
        else:
            return JsonResponse({'attributes': None})

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
