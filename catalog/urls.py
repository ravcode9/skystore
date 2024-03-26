from django.urls import path
from .views import index, contact, product_detail
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('contact/', contact, name='contact'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
]
