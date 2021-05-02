from django.db import models
from apps.catalog import models as custom_models
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.db.models import Max, Min


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
    def get_filters(cls, products):
        price_info = products.aggregate(min_value=Min('price'),
            max_value=Max('price'))
        price_min = int(price_info['min_value'])
        price_max = int(price_info['max_value'])
        data = {
            'attributes': cls._attributes_for_filtering(products),
            'price_min': price_min,
            'price_max': price_max
        }
        return data

    @staticmethod
    def _attributes_for_filtering(products):
        attributes = list(custom_models.ProductAttributeValue.objects.filter(product__in=products).distinct())
        filter_titles = {}
        filter_values = {}
        result = {}
        for item in attributes:
            attr_id, title = item.attribute_value.attribute.id_1c, item.attribute_value.attribute.title
            filter_titles[attr_id] = title

        for item in attributes:
            attr_id, value = item.attribute_value.attribute.id_1c, item.attribute_value.value
            filter_values[attr_id] = value
        result['titles'] = filter_titles
        result['values'] = filter_values
        return result
