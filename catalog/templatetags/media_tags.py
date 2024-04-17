from django import template

register = template.Library()


@register.filter
def media_url(path):
    if path:
        return f'/media/{path}'
    return '/static/product.jpg'


@register.filter
def get_active_version(product_versions, product):
    return product_versions.get(product)
