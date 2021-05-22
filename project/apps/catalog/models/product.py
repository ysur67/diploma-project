from django.db import models
from django.db.models.query import QuerySet
from apps.catalog import models as custom_models
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.db.models import Max, Min
# from .attibute import Attribute, AttributeValue, ProductAttributeValue
from .. import models as custom_models


class Product(custom_models.CatalogMixin):
    code = models.CharField(
        max_length=200,
        verbose_name='Артикул',
        null=True
    )
    category = models.ForeignKey(
        custom_models.Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Категория',
        null=True,
        blank=True,
    )
    price = models.DecimalField(
        null=False,
        blank=False,
        default=0,
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0)
        ],
        verbose_name='Текущая цена'
    )
    amount = models.IntegerField(
        null=False,
        blank=False,
        default=0,
        validators=[
            MinValueValidator(0)
        ],
        verbose_name='Количество товара'
    )
    old_price = models.DecimalField(
        null=False,
        blank=False,
        default=0,
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0)
        ],
        verbose_name='Старая цена'
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("catalog:product_detail", kwargs={
            "product_slug": self.slug})

    @classmethod
    def get_filters(cls, product_qs: QuerySet) -> list:
        """
        Retruns list of related filters

        `product_qs` -> QuerySet of Product objects
        """
        # Получаем все Товар-Атрибут-Значения исходя из товаров в запросе
        product_attribute_value = custom_models.ProductAttributeValue.objects.filter(
            product__in=product_qs
        )
        # Получаем все Атрибут-Значения исходя из полученных выше
        attribute_values = custom_models.AttributeValue.objects.filter(
            products__in=product_attribute_value
        ).distinct('value')
        # Получаем все названия атрибутов
        titles = attribute_values.distinct('attribute')
        # Пытаемся создать словарь ТайтлАтрибута = [Значения атрибута]
        filter_list = []
        for attribute_value in titles:
            filter_ = custom_models.FilterSet(attribute_value.attribute.title)
            for value in attribute_values.filter(attribute=attribute_value.attribute):
                filter_.set_value(value)
            filter_list.append(filter_)
        return filter_list

    @classmethod
    def filter_products(cls, products_qs: QuerySet, request) -> QuerySet:
        values_list = request.GET.getlist('value')

        if values_list:
            products_qs = products_qs.filter(
                attributes__attribute_value__id__in=values_list
            )

        return products_qs, values_list
