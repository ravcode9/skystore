from django.urls import path
from catalog.views import ProductListView, ProductDetailView, ContactView
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]