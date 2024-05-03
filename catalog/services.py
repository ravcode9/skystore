from django.core.cache import cache
from .models import Category
from django.conf import settings


def get_categories():
    if settings.CACHE_ENABLED:
        key = 'categories'
        categories = cache.get(key)
        if not categories:
            categories = Category.objects.all()
            cache.set(key, categories)
        return categories
    else:
        return Category.objects.all()
