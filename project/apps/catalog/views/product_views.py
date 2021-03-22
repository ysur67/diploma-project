from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from apps.catalog.models import Product, Category
from rest_framework.views import APIView
from apps.catalog.serializers import (
    ProductDetailSerializer, 
    ProductListSerializer
    )
from rest_framework.response import Response
from rest_framework import generics, viewsets
from django.shortcuts import get_object_or_404 


class ProductDetail(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    slug_url_kwarg = 'product_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(slug=self.kwargs['product_slug'])
        similar_products = Product.objects.filter(category=context['product'].category)
        context['similar_products'] = similar_products.exclude(slug=context['product'].slug)
        return context


class ProductRestViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(active=True)
    serializer_class = ProductDetailSerializer

    def perform_create(self, serializer):
        serializer.save()