from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse
from apps.catalog import models as custom_models


class Category(MPTTModel, custom_models.CatalogMixin):

    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True, 
        related_name='children',
        verbose_name='Родитель'
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории товаров"

    def __str__(self):
        return self.title

    def get_active_children(self):
        return self.get_children().filter(products__gt=0).distinct()

    def get_absolute_url(self):
        return reverse("catalog:category_detail", kwargs={"slug": self.slug})

    @classmethod
    def get_products(self, instance):
        qs = custom_models.Product.objects.filter(
            category__in=instance.get_descendants(include_self=True),
        )
        qs = qs.distinct()

        return qs.order_by("-id")


