# -*- encoding: utf-8 -*-
from django.shortcuts import redirect
from datetime import datetime
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    TemplateView,
    ListView,
    DeleteView,
    CreateView,
    DetailView,
)

from applications.almacen.recepcion.models import DetailGuide

from .functions import calcular_resumen

from .forms import NotaForm

from .models import LostMagazine, DetailBoleta, Boleta

class PanelAdmin(TemplateView):
    """panel del administrador"""
    template_name = 'admin/panel.html'

    def get_context_data(self, **kwargs):
        context = super(PanelAdmin, self).get_context_data(**kwargs)
        ####optimmizar
        context['resumen'] = calcular_resumen()
        return context


class NotaCreditoView(FormView):
    """vista para crear una nota de credito"""
    form_class = NotaForm
    success_url = '.'
    template_name = 'admin/nota.html'

    def form_valid(self,form):
        #traemos los datos
        guide = form.cleaned_data['guide']
        magazine_day = form.cleaned_data['magazine_day']
        precio_guia = form.cleaned_data['precio_guia']
        precio_venta = form.cleaned_data['precio_venta']
        #recuperamos la guia detalle a descontar
        dg = DetailGuide.objects.get(
            pk=magazine_day,
        )
        #creamos el descuento
        detail_guide = DetailGuide(
            magazine_day=dg.magazine_day,
            guide=dg.guide,
            count=dg.count,
            precio_unitario=precio_venta,
            precio_guia=precio_guia,
            precio_tapa=dg.precio_tapa,
            precio_sunat=dg.precio_sunat,
            discount=True,
            user_created=self.request.user,
        )
        detail_guide.save()
        return super(NotaCreditoView, self).form_valid(form)


class PanelControl(TemplateView):
    template_name = 'admin/control/panel.html'


class ProductosBoleta(TemplateView):
    '''
        lista magazins a imprimr en boleta
    '''
    template_name = 'admin/contabilidad/list.html'


class BoletasEmitidas(TemplateView):
    '''Lista de boletas emitidas'''
    template_name = 'admin/contabilidad/emitidos.html'


class BoletasDetailView(DeleteView):
    '''lista los items de una boleta emitida'''
    template_name = 'admin/contabilidad/item_boleta.html'
    model = Boleta
    success_url = success_url = reverse_lazy('administrador_app:contabilidad-emitido')

    def get_context_data(self, **kwargs):
        context = super(BoletasDetailView, self).get_context_data(**kwargs)
        boleta = self.kwargs.get('pk',0)
        queryset = DetailBoleta.objects.filter(
            boleta__pk=boleta,
        )
        context['list_item_boleta'] = queryset
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.anulate = True
        self.object.user_modified = self.request.user
        self.object.save()
        #recuperamos los items y cambiamos estados
        detalis = DetailBoleta.objects.filter(
            anulate=False,
            boleta__pk=self.object.pk,
        )
        detalis.delete()
        return HttpResponseRedirect(
            reverse(
                'administrador_app:contabilidad-emitidos'
            )
        )


class ControlMagazins(TemplateView):
    '''
        registro de control de diairos productos
    '''
    template_name = 'admin/control/magazins.html'


class ControlMagazinsList(TemplateView):
    '''
        Lista de Control de Diarios y Productos
    '''
    template_name = 'admin/control/magazins_list.html'


class LostMagazineDeleteView(DeleteView):
    model = LostMagazine
    template_name = 'admin/control/magazins_delete.html'
    success_url = success_url = reverse_lazy('administrador_app:control-list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.anulate = True
        self.object.user_modified = self.request.user
        self.object.save()
        success_url = self.get_success_url()

        return HttpResponseRedirect(success_url)
