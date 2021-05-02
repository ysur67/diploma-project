from django.db import models
from apps.catalog.models import Product


class Attribute(models.Model):
    id_1c = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        unique=True,
        verbose_name="Идентификатор из базы 1с"
    )
    title = models.CharField(
        max_length=300,
        null=False,
        blank=False,
        verbose_name='Наименование'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Свойство \ Атрибут'
        verbose_name_plural = 'Свойства \ Атрибуты'
    

class AttributeValue(models.Model):
    id_1c = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        unique=True,
        verbose_name="Идентификатор из базы 1с"
    )
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        verbose_name='Атрибут',
        related_name='values',
    )
    value = models.CharField(
        max_length=300,
        null=False,
        blank=False,
        verbose_name='Значение'
    )
    
    def __str__(self):
        return str(self.attribute) + ': ' + str(self.value)

    class Meta:
        verbose_name = 'Значение свойства'
        verbose_name_plural = 'Значния свойств'
    


class ProductAttributeValue(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар',
        related_name='attributes',
        null=True,
    )
    attribute_value = models.ForeignKey(
        AttributeValue,
        on_delete=models.CASCADE,
        verbose_name='Атрибут и его значение',
        related_name='products',
        null=True,
    )

    def __str__(self):
        return str(self.product) + \
            ': ' + str(self.attribute_value)

    class Meta:
       verbose_name = 'Значние свойства товара'
       verbose_name_plural = 'Значения свойств товаров'


class FilterSet:
    """Represents a filter set, that
    should be generated when 
    you've taken the values

    {title} - Attribute title
    {values} - All the values
    of attribute
    """
    def __init__(self, title: str, values=None):
        self.title = title
        self.values = values if values is not None\
            else []
    
    def set_value(self, value):
        self.values.append(value)
