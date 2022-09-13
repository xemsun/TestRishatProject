from django.core.management import BaseCommand

from item.models import Item


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Item.objects.all().delete()
        item = Item.objects.create(name='Test Item', description='Lalal', price='1000')
        item.save()
