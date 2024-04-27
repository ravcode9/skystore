from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from catalog.forms import ProductForm, VersionForm, ProductModeratorForm
from catalog.models import Product, Version


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    permission_required = 'catalog.view_product'
    template_name = 'catalog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()
        product_versions = {}
        for product in products:
            active_version = Version.objects.filter(product=product, is_current=True).first()
            product_versions[product] = active_version
        context['product_versions'] = product_versions
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    permission_required = 'catalog.view_product'
    template_name = 'catalog/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.object
        return context


class ContactView(LoginRequiredMixin, TemplateView):
    template_name = 'catalog/contact.html'


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    permission_required = 'catalog.add_product'
    success_url = reverse_lazy('catalog:index')

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:index')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            formset = VersionFormset(self.request.POST, instance=self.object)
        else:
            formset = VersionFormset(instance=self.object)
        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        if formset.is_valid():
            formset.save()
        return super().form_valid(form)

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner or user.has_perm('catalog.can_edit_product') or user.has_perm(
                'catalog.can_edit_description') or user.has_perm('catalog.can_edit_is_published') or user.is_superuser:
            return ProductForm
        raise PermissionDenied

    def dispatch(self, request, *args, **kwargs):
        if (request.user != self.get_object().owner and not request.user.is_superuser and not request.user.has_perm('catalog.can_edit_product')
                and not request.user.has_perm('catalog.can_edit_description') and not request.user.has_perm('catalog.can_edit_is_published')):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:index')
    template_name = 'catalog/product_confirm_delete.html'

    def test_func(self):
        return self.request.user.is_superuser
