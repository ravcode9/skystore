from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.CharField(max_length=150, null=True, blank=True, verbose_name='Слаг')
    content = models.TextField(verbose_name='Содержимое')
    preview_image = models.ImageField(upload_to='blog_images/', null=True, blank=True, verbose_name='Превью')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    published = models.BooleanField(default=False, verbose_name='Опубликовано')

    views_count = models.IntegerField(default=0, verbose_name='просмотры')
    is_published = models.BooleanField(default=True, verbose_name='опубликовано')

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'

    def __str__(self):
        return self.title

