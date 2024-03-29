from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView

from catalog.models import Product


# Create your views here.


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/index.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'


class ContactView(TemplateView):
    template_name = 'catalog/contact.html'

