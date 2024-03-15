from django.core.management.base import BaseCommand
from catalog.models import Product, Category
import json


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        with open('catalog/fixtures/categories_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def json_read_products():
        with open('catalog/fixtures/products_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)

    def handle(self, *args, **options):
        # Удаление всех продуктов и категорий
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Создание категорий
        categories_data = Command.json_read_categories()
        categories_mapping = {}
        for category_data in categories_data:
            category = Category.objects.create(name=category_data['fields']['name'])
            categories_mapping[category_data['pk']] = category

        # Создание продуктов
        products_data = Command.json_read_products()
        for product_data in products_data:
            category_id = product_data['fields']['category']
            category = categories_mapping[category_id]
            product_data['fields']['category'] = category  # Заменяем идентификатор категории объектом категории
            Product.objects.create(**product_data['fields'])
