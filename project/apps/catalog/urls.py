from django.urls import path
from .views import (
    CatalogView, 
    ProductDetail,
    ProductRestViewSet,
    CategoryJSONDetail, 
    CategoryRestViewSet,
)
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'api/products', ProductRestViewSet, basename='product')
router.register(r'api/category', CategoryRestViewSet, basename='category')


app_name = 'catalog'

urlpatterns = [
    path('catalog/', CatalogView.as_view(), name='category_list'),
    path('catalog/<slug>/', CategoryJSONDetail.as_view(), name='category_detail'),
    path('product/<product_slug>/',ProductDetail.as_view(), name='product_detail'),
]

urlpatterns += router.urls
