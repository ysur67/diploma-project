from django.core.management.base import BaseCommand, CommandError
from apps.catalog.models import Product
import random


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.insert_products()

    def insert_products(self):
        products = Product.objects.filter(price__gt=0)
        
        for product in products:
            value = random.randint(1, 25)
            product.amount = value
            print(f"""
            Товар - {product.title}
            Количество = {product.amount}
            """)
            product.save()