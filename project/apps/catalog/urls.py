from django.urls import path
from .views import (
    CatalogView, 
    ProductDetail,
    ProductRestViewSet,
    CategoryJSONDetail, 
    SearchAPIView,
    SearchJSONView
)
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter


# router = DefaultRouter()
# router.register(r'api/category', CategoryRestViewSet, basename='category')


app_name = 'catalog'

urlpatterns = [
    path('catalog/', CatalogView.as_view(), name='category_list'),
    path('catalog/<slug>/', CategoryJSONDetail.as_view(), name='category_detail'),
    path('catalog/search/', SearchJSONView.as_view(), name='search_result'),
    path('product/<product_slug>/', ProductDetail.as_view(), name='product_detail'),
    path('api/products/<slug>/', ProductRestViewSet.as_view(), name='api_product_list'),
    path('api/catalog/', SearchAPIView.as_view(), name='api_catalog_search')
    # path('api/filterset/<slug>/', FilterViewSet.as_view({'post': 'list'}), name='api_filter_set')
]

# urlpatterns += router.urls
