from django.core.management import BaseCommand
from catalog.models import Product, Category


class Command(BaseCommand):

    def handle(self, *args, **options):
        products_list = [
            {'name': 'картофель', 'price': '50', 'category_name': 'овощ', 'description': 'всегда пригодится'},
            {'name': 'помидор', 'price': '60', 'category_name': 'овощ', 'description': ''},
            {'name': 'банан', 'price': '90', 'category_name': 'фрукт', 'description': 'полезный перекус'},
            {'name': 'яблоко', 'price': '70', 'category_name': 'фрукт', 'description': ''}
        ]

        products_for_create = []
        for product_item in products_list:
            category_name = product_item.pop('category_name')
            category, created = Category.objects.get_or_create(name=category_name)
            product_item['category'] = category
            products_for_create.append(Product(**product_item))

        Product.objects.bulk_create(products_for_create)
