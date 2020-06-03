# -*- encoding: utf-8 -*-
from django.shortcuts import render
from datetime import datetime, timedelta
from django.utils import timezone
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

from applications.almacen.recepcion.models import (
    Magazine,
    MagazineDay,
    DetailGuide,
)
from .models import Asignation, DetailAsignation, DetailPauta
from applications.caja.pagos.models import Payment


class MagazineDeliverListView(ListView):
    '''Lista de diarios por entregar'''

    context_object_name = 'magazin_list'
    template_name = 'almacen/asignacion/entrega/list.html'

    def get_context_data(self, **kwargs):
        context = super(MagazineDeliverListView, self).get_context_data(**kwargs)
        #recuperamos el evento (pauta=0 o registro=1)
        context['key'] = self.kwargs.get('pk',0)
        return context

    def queryset(self):
        queryset = DetailGuide.objects.magazine_no_expired('0')

        return queryset


class MagazineListDeliverView(TemplateView):
    '''Lista de diarios por entregar'''
    template_name = 'almacen/asignacion/entrega/list2.html'


class ProductDeliverListView(ListView):
    '''Lista de productos por entregar'''

    context_object_name = 'magazin_list'
    template_name = 'almacen/asignacion/entrega/prod_list.html'

    def queryset(self):
        queryset = DetailGuide.objects.magazine_no_expired('1')

        return queryset


class DetailGuideDetailView(DetailView):
    ''' Vista para Registrar una Entrega o Generar una Pauta '''
    model = DetailGuide
    template_name = 'almacen/asignacion/entrega/add.html'

    def get_context_data(self, **kwargs):
        context = super(DetailGuideDetailView, self).get_context_data(**kwargs)
        tipo = self.kwargs.get('key',0)
        #si el diario ya tiene al menos un pago no se podra modificar
        aux = Payment.objects.filter(
            detail_asignation__asignation__detail_guide=self.object,
            anulate=False,
        ).count()
        if aux > 0:
            #no se puede modificar
            tipo = '2'

        context['tipo'] = tipo
        return context


class ProdDetailGuideDetailView(DetailView):
    ''' Vista para Registrar una Entrega un producto '''
    model = DetailGuide
    template_name = 'almacen/asignacion/entrega/add_prod.html'

    def get_context_data(self, **kwargs):
        context = super(ProdDetailGuideDetailView, self).get_context_data(**kwargs)
        tipo = self.kwargs.get('key',0)
        #si el diario ya tiene al menos un pago no se podra modificar
        aux = Payment.objects.filter(
            detail_asignation__asignation__detail_guide=self.object,
            anulate=False,
        ).count()
        if aux > 0:
            #no se puede modificar
            tipo = '2'

        context['tipo'] = tipo
        return context


class PautaDeliverView(DetailView):
    ''' Vista para Registrar una una Pauta '''
    model = DetailGuide
    template_name = 'almacen/asignacion/entrega/prod_add.html'


class ListaConsultaView(TemplateView):
    template_name = 'almacen/asignacion/consulta/list.html'


class DetailConsultaView(DetailView):
    model = Asignation
    template_name = 'almacen/asignacion/consulta/view.html'


class PautaDinamicaView(TemplateView):
    template_name = 'almacen/asignacion/entrega/pauta-dinamica.html'


class AddEntregaProducto(TemplateView):
    template_name = 'almacen/asignacion/entrega/producto_registrar.html'


class PautaDeleteListView(ListView):
    '''Lista de productos que se pueden eliminar'''

    context_object_name = 'lista_asignados'
    template_name = 'almacen/asignacion/entrega/list_delete_prod.html'

    def queryset(self):
        cod = self.kwargs.get('cod',0)
        tipo = self.kwargs.get('tipo',0)
        lista = DetailPauta.objects.list_ultimos_registros(cod,tipo)
        #verificamos si ya tiene pagos
        resultado = []
        for l in lista:
            if Payment.objects.filter(detail_asignation__asignation__detail_guide=l.pauta.detail_guide).exists() == False:
                resultado.append(l)

        return resultado


class PautaDeleteView(DeleteView):
    """vista para eliminar un producto"""
    model = DetailPauta
    template_name = 'almacen/asignacion/entrega/delete_asig_prod.html'
    success_url = reverse_lazy('asignacion_app:entrega-prod_add')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.asignado = False
        self.object.user_modified = self.request.user
        self.object.save()
        #
        detail_pauta = self.object
        #eliminamos la asignacion real
        detail_asignation = DetailAsignation.objects.filter(
            anulate=False,
            vendor=self.object.vendor,
            asignation__detail_guide=detail_pauta.pauta.detail_guide,
        )
        detail_asignation.delete()
        #
        if detail_pauta.pauta.detail_guide.magazine_day.magazine.tipo == '1':
            return HttpResponseRedirect(
                reverse(
                    'asignacion_app:entrega-prod_add',
                )
            )
        else:
            return HttpResponseRedirect(
                reverse(
                    'asignacion_app:entrega-diario_dni',
                )
            )


class PautaDiarioView(DetailView):
    ''' Vista para Registrar una una Pauta '''
    model = DetailGuide
    template_name = 'almacen/asignacion/entrega/diario/pauta_diario.html'


class AddEntregaDiario(TemplateView):
    template_name = 'almacen/asignacion/entrega/diario/entrega_diario.html'
