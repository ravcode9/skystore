from django import template

register = template.Library()


@register.filter
def media_url(path):
    if path:
        return f'/media/{path}'
    return '/static/product.jpg'
