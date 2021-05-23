from django.views.generic.base import View
from django.views.generic.detail import DetailView, SingleObjectTemplateResponseMixin
from apps.main.views import JSONDetailView, JSONResponseMixin
from django.views.generic.list import ListView
from apps.catalog.models import (
    Category,
    Product,
    AttributeValue,
    Attribute,
    FilterSet,
    ProductAttributeValue
)
from django.http import JsonResponse
from django.template.loader import get_template
from apps.main.utils import pagination


class CatalogView(ListView):
    model = Category
    template_name = 'catalog/catalog.html'

    def get_queryset(self, *args, **kwargs):
        return Category.objects.filter(active=True, parent=None)


class CategoryJSONDetail(SingleObjectTemplateResponseMixin, JSONDetailView):
    model = Category
    context_object_name = 'category'
    template_name = 'catalog/product_list.html'

    def render_to_response(self, context, **response_kwargs):
        obj = context['object']
        request = self.request
        products = self.model.get_products(obj)
        if self.request.is_ajax():
            context['filters'] = Product.get_filters(products)
            products, _ = Product.filter_products(products, request)
        products_count = products.count()
        context['total'] = products_count
        context['tile'] = False
        display_type = request.session.get('display_type', None)
        if display_type == 'tile':
            context['tile'] = True
        if products_count:
            try:
                page = int(request.GET.get('page', 1))
            except ValueError:
                page = 1

            pagin = pagination(products, page, 12, count=context['total'])
            products = pagin.items
            context['pagination'] = get_template(
                "includes/pagination.html"
            ).render({'PAGIN': pagin})
            if products_count <= 10:
                context['pagination'] = None
            products_template = []
            for product in products:
                products_template.append(
                    get_template('catalog/includes/product.html').render({
                        'product': product,
                    })

                )
            context['products'] = products_template

        if self.request.is_ajax():     
            context['template_filters'] = get_template(
                'catalog/includes/filters.html'
            ).render({
                'attribute_list': context['filters'],
            })
            del (context["object"], context["view"], context['category'], context['filters'])
            return self.render_to_json_response(context, **response_kwargs)

        if not self.request.is_ajax():
            del products
            return super().render_to_response(context, **response_kwargs)


class SearchAPIView(View):
    def post(self, request, *args, **kwargs):
        post_data = request.POST
        search_string = post_data.get('search', None)
        json_respone = {}
        if not search_string:
            json_respone['errors'] = False
            json_respone['template'] = "По вашему запросу не найдено товаров"
        
        if search_string:
            qs = Product.objects.filter(title__icontains=search_string).order_by('?')[:10]
            if not qs.exists():
                json_respone['template'] = "По вашему запросу не найдено товаров"
                return JsonResponse(json_respone)
            template = get_template('catalog/search.html').render({
                'products': qs
            })
            json_respone['errors'] = False
            json_respone['template'] = template

        return JsonResponse(json_respone)


class SearchJSONView(CategoryJSONDetail):

    def get_qs(self, context):
        request = self.request
        post_data = request.POST
        search = post_data.get('search', None)
        if search:
            qs = Product.objects.filter(
                title__icontains=search
            )
        return qs
