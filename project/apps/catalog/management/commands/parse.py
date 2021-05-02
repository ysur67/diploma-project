import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand, CommandError
from apps.catalog.models import Category, Attribute, AttributeValue, ProductAttributeValue, Product
from django.db.utils import IntegrityError
from decimal import *
from django.conf import settings
from pathlib import Path
from pytils.translit import slugify


class Command(BaseCommand):  
    """ Starts parser """

    def handle(self, *args, **options):
        """ Calls parser's class"""
        Parser()


class Parser():
    """Parses both of import files
    inside 'imports/' folder"""
    def __init__(self):
        """Gets import file, then needed values"""
        base_dir = settings.BASE_DIR
        tree = ET.parse(base_dir / '../' / 'imports/import.xml')
        root = tree.getroot()
        ks = root.find("Классификатор")
        groups = ks.find("Группы")
        for group in groups.findall('Группа'):
            self.set_groups(group)
        properties = ks.find('Свойства')
        for property_ in properties.findall('Свойство'):
            self.set_properties_and_values(property_)
        main_catalog = root.find('Каталог')
        product_list = main_catalog.find('Товары')
        for product in product_list.findall('Товар'):
            self.set_products(product)
        offer_tree = ET.parse(base_dir / '../' / 'imports/offers.xml')
        offer_root = offer_tree.getroot()
        offers_pack = offer_root.find('ПакетПредложений')
        offers_block = offers_pack.find('Предложения')
        for offer in offers_block.findall('Предложение'):
            self.set_prices(offer)

    def set_groups(self, group, parent_id=None):
        """Creates rows in Category by given values

        { group } - category from import file

        { parent_id } - id of parent category
        """
        title = group.find('Наименование').text
        group_id = group.find('Ид').text
        category, made_now = Category.objects.get_or_create(id_1c=group_id)
        category.title = title
        print(f'Категория: {str(category)}')
        if parent_id:
            parent = Category.objects.get(id_1c=parent_id)
            category.parent = parent
            print(f'\tРодитель: {parent}')
        try:
            category.set_slug()
            category.save()
        except IntegrityError:
            category.set_unique_slug()
            category.save()
        children = group.find('Группы')
        if children is not None:
            subs = children.findall('Группа')
            for sub in subs:
                self.set_groups(sub, parent_id=group_id)

    def set_properties_and_values(self, property_):
        """Creates rows in Attribute and Value tables
        by given values

        { property_ } - attribute from import file
        """
        title = property_.find('Наименование').text
        prop_id = property_.find('Ид').text
        attribute, made_now = Attribute.objects.get_or_create(id_1c=prop_id)
        attribute.title = title
        attribute.save()
        print(f'Атрибут: {str(attribute.title)}')
        prop_values = property_.find('ВариантыЗначений')
        if prop_values is not None:
            values = prop_values.findall('Справочник')
            for value in values:
                value_title = value.find('Значение').text
                value_id = value.find('ИдЗначения').text
                attr_value = AttributeValue.objects.update_or_create(
                    id_1c=value_id,
                    attribute=attribute,
                    value=value_title
                )
                print(f'Значение атрибута {attribute}: {value_title}')

    def set_products(self, product):
        """Creates row in Product table
        by given values

        { product } - product from import file
        """
        product_id = product.find('Ид').text
        product_code = product.find('Артикул')
        product_title = product.find('Наименование').text
        product_group = product.find('Группы').find('Ид').text
        product_image = product.find('Картинка')
        product_desc = product.find('Описание')
        product_attributes = product.find('ЗначенияСвойств')
        try:
            product = Product.objects.create(id_1c=product_id)
        except IntegrityError:
            product = Product.objects.get(id_1c=product_id)
        product.title = product_title
        if product_code is not None:
            product.code = product_code.text
        product.category = Category.objects.get(id_1c=product_group)
        if product_image is not None:
            product.image = product_image.text
        if product_desc is not None:
            product.description = product_desc.text
        try:
            product.set_slug()
            product.save()
        except IntegrityError:
            product.set_unique_slug()
            product.save()
        if product_attributes:
            self.set_product_properties(product, product_attributes)

    def set_product_properties(self, product, attributes):
        """Creates rows in ProductAttributeValue table
        by given values

        { product } - product from import file

        { attributes } - ids of product's attributes from import file
        """
        for attribute in attributes.findall('ЗначенияСвойства'):
            value = attribute.find('Значение').text
            value_id = attribute.find('Ид').text
            if value is not None:
                try:
                    attribute_value = AttributeValue.objects.get(id_1c=value)
                except Exception as e:
                    print(e)
                    print(value)
                product_attr = ProductAttributeValue.objects.update_or_create(
                    product=product,
                    attribute_value=attribute_value
                )
                print(f"Товар {str(product)}")
                print(f"Значение {str(attribute_value)}")

        
    def set_prices(self, offer):
        """Sets retail price for product

        { offer } - offer from import file

        Has retail_id inside, because others
        aren't needed
        """
        retail_id = "9243451b-d222-49a3-b0f8-134cce762863"
        product_id = offer.find('Ид').text
        prices = offer.find('Цены')
        if prices is not None:
            for price in prices.findall('Цена'):
                price_id = price.find('ИдТипаЦены').text
                if price_id == retail_id:
                    price_value = price.find('ЦенаЗаЕдиницу').text
                    product = Product.objects.get(id_1c=product_id)
                    product.price = Decimal(price_value)
                    product.save()
                    print(f'Товар: {str(product)}')
                    print(f'\t Цена: {str(product.price)}')
