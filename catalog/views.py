from django.shortcuts import render

from catalog.models import Product


# Create your views here.


def index(request):
    product_list = Product.objects.all()
    context = {
        'object_list': product_list,
        'title': 'Главная'
    }
    return render(request, 'catalog/index.html', context)


def contact(request):
    context = {
        'title': 'Контакты'
    }
    return render(request, 'catalog/contact.html', context)


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    context = {'product': product}

    # Проверяем, есть ли у продукта изображение
    if product.image:
        # Если у продукта есть изображение, передаем URL изображения в контекст
        context['product_image_url'] = product.image.url

    return render(request, 'catalog/product_detail.html', context)

