from django.core.management.base import BaseCommand, CommandError
from apps.catalog.models import AttributeValue


class Command(BaseCommand):
    def handle(self, *args, **options):
        AttributeValue.objects.all().delete()

