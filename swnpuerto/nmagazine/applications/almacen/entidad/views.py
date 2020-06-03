# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.views.generic import (
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
    ListView,
    TemplateView,
    View,
)

from .models import Provider, Vendor
from .forms import ProviderForm, VendorForm
from .functions import execute_scrip

# Create your views here.
class ProviderCreateView(CreateView):
    '''registrar un proveedor'''
    form_class = ProviderForm
    success_url = success_url = reverse_lazy('entidad_app:provider-list')
    template_name = 'almacen/entidad/proveedor/add.html'

    def form_valid(self, form):
        provider = form.save(commit=False)
        provider.user_created = self.request.user
        provider.save()

        return super(ProviderCreateView, self).form_valid(form)


class ProviderUpdateView(UpdateView):
    '''modificar proveedor'''
    model = Provider
    form_class = ProviderForm
    success_url = reverse_lazy('entidad_app:provider-list')
    template_name = 'almacen/entidad/proveedor/update.html'

    def form_valid(self, form):
        form.save()
        proveedor = self.get_object()
        proveedor.user_modified = self.request.user
        proveedor.save()

        return super(ProviderUpdateView, self).form_valid(form)


class ProviderDetailView(DetailView):
    model = Provider
    template_name = 'almacen/entidad/proveedor/detail.html'


class ProviderDeleteView(DeleteView):
    model = Provider
    success_url = reverse_lazy('entidad_app:provider-list')
    template_name = 'almacen/entidad/proveedor/delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.disable = True
        self.object.user_modified = self.request.user
        self.object.save()
        success_url = self.get_success_url()

        return HttpResponseRedirect(success_url)


class ProviderListView(ListView):
    context_object_name = 'provider_list'
    template_name = 'almacen/entidad/proveedor/list.html'

    def get_queryset(self):
        return Provider.objects.filter(disable=False)


class VendorListView(TemplateView):
    template_name = 'almacen/entidad/vendor/list.html'


class VendorCreateView(CreateView):
    '''registrar un proveedor'''
    form_class = VendorForm
    success_url = success_url = reverse_lazy('entidad_app:vendor-list')
    template_name = 'almacen/entidad/vendor/add.html'

    def form_valid(self, form):
        vendor = form.save(commit=False)
        vendor.user_created = self.request.user
        vendor.save()

        return super(VendorCreateView, self).form_valid(form)

class VendorUpdateView(UpdateView):
    '''modificar vendor'''
    model = Vendor
    form_class = VendorForm
    success_url = reverse_lazy('entidad_app:vendor-list')
    template_name = 'almacen/entidad/vendor/update.html'

    def form_valid(self, form):
        form.save()
        canilla = self.get_object()
        canilla.user_modified = self.request.user
        canilla.save()

        return super(VendorUpdateView, self).form_valid(form)


class VendorDetailView(DetailView):
    model = Vendor
    template_name = 'almacen/entidad/vendor/detail.html'


class VendorDeleteView(DeleteView):
    model = Vendor
    success_url = success_url = reverse_lazy('entidad_app:vendor-list')
    template_name = 'almacen/entidad/vendor/delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.anulate = True
        self.object.user_modified = self.request.user
        self.object.save()
        success_url = self.get_success_url()

        return HttpResponseRedirect(success_url)


class VendorDisbleView(DeleteView):
    model = Vendor
    success_url = success_url = reverse_lazy('entidad_app:vendor-list')
    template_name = 'almacen/entidad/vendor/disable.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.disable = True
        self.object.user_modified = self.request.user
        self.object.save()
        success_url = self.get_success_url()

        return HttpResponseRedirect(success_url)


class VendorEnabledView(DeleteView):
    model = Vendor
    success_url = success_url = reverse_lazy('entidad_app:vendor-list')
    template_name = 'almacen/entidad/vendor/enabled.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.disable = False
        self.object.user_modified = self.request.user
        self.object.save()
        success_url = self.get_success_url()

        return HttpResponseRedirect(success_url)


class LoginTemplateView(TemplateView):
    template_name = 'users/login/login.html'


class HomeTemplateView(TemplateView):
    template_name = 'base/dashboardAlmacen.html'


class ScripTemplateView(TemplateView):
    template_name = 'almacen/entidad/scrip.html'

    def get_context_data(self, **kwargs):
        context = super(ScripTemplateView, self).get_context_data(**kwargs)
        rango = self.kwargs.get('pk',0)
        context['resultado'] = execute_scrip(rango)
        return context
