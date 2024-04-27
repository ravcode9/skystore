
from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.CharField(max_length=200, verbose_name='Описание')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = "Категории"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.CharField(max_length=200, verbose_name='Описание', **NULLABLE)
    image = models.ImageField(upload_to='product_images/', verbose_name='Изображение (превью)', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за покупку')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')
    owner = models.ForeignKey(User, verbose_name='Владелец', help_text='Укажите владельца продукта', on_delete=models.SET_NULL, **NULLABLE)
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = "Продукты"
        permissions = [
            ('can_edit_product', 'Can edit product'),
            ('can_edit_description', 'Can edit description'),
            ('can_edit_is_published', 'Can edit is_published')
        ]

    def __str__(self):
        return f'{self.name}, {self.price}'


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='versions', verbose_name='Продукт')
    version_number = models.CharField(max_length=50, verbose_name='Номер версии')
    version_name = models.CharField(max_length=100, verbose_name='Название версии')
    is_current = models.BooleanField(default=False, verbose_name='Текущая версия')

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'

    def __str__(self):
        return f'{self.product.name} - {self.version_number}'

    def save(self, *args, **kwargs):
        if self.is_current:
            Version.objects.filter(product=self.product).exclude(id=self.id).update(is_current=False)
        super().save(*args, **kwargs)
