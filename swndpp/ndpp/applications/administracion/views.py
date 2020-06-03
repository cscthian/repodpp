# -*- coding: utf-8 -*-
from django.shortcuts import render
import operator
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

#app miscelanea
from applications.miscelanea.models import Vendor
#app recepcion
from applications.recepcion.models import DetailGuide, Guide

#app Caja
from applications.caja.models import Payment
#
from applications.caja.functions import (
    deuda_magazine_agente,
    deuda_magazine_agente_total,
    deuda_magazine_agente_detalle
)

#aplicacion reporte
from applications.reportes.models import Voucher, NotaCredito

#formulario
from .forms import (
    FilterForm,
    FilterProviderLiquidacion,
    ProviderLiquidacionForm,
    BoletaFilterForm,
    SearchGuidesForm
)

#
from .models import Boleta, DetailBoleta

#funciones
from .functions import (
    movimientos_by_guia_by_departamento,
    movimientos_by_guia_by_departamento_facturado,
    history_guide,
)

class AdministracionReporte(TemplateView):
    template_name = 'administracion/reportes/index.html'


class ListaGuiaReporte(ListView):
    """ lista guias modulo reportes """
    context_object_name = 'guias'
    template_name = 'administracion/reportes/guia/list.html'

    def get_context_data(self, **kwargs):
        context = super(ListaGuiaReporte, self).get_context_data(**kwargs)
        context['form'] = FilterForm
        return context

    def get_queryset(self):
        q = self.request.GET.get("date_start", '')
        r = self.request.GET.get("date_end", '')
        s = self.request.GET.get("number", '')
        t = self.request.GET.get("state", '')
        queryset = DetailGuide.objects.filter_guide(q,r,s,t)
        return queryset


class ListaFacturaReporte(ListView):
    """ lista guias modulo reportes """
    context_object_name = 'consulta'
    template_name = 'administracion/reportes/factura/facturas.html'

    def get_context_data(self, **kwargs):
        context = super(ListaFacturaReporte, self).get_context_data(**kwargs)
        context['form'] = FilterForm
        return context

    def get_queryset(self):
        q = self.request.GET.get("date_start", '')
        r = self.request.GET.get("date_end", '')
        s = self.request.GET.get("number", '')
        t = self.request.GET.get("state", '')
        facturas = Voucher.objects.filter_factura(q,r,s,t)
        notas = NotaCredito.objects.filter_nota(q,r)
        #devolvemos diccionario de facturas y notas de credito
        return {'facturas':facturas,'notas':notas}


class LiquidacionProveedorReporte(TemplateView):
    """ lista los movimiento de una guia desde su llegada compra total"""

    template_name = 'administracion/reportes/ventas/list.html'


class LiquidacionFacturaProveedorReporte(TemplateView):
    """ lista los movimiento de una factura"""

    template_name = 'administracion/reportes/ventas/lista_factura.html'
    #     queryset = movimientos_by_guia_by_departamento_facturado(q,r,s,t)
    #     return {'consulta':queryset[0],'total':queryset[1]}


class LiquidacionRegistrarPagoReporte(TemplateView):
    template_name = 'administracion/procesos/pagar_facturas.html'


class SeguimientoAgentesView(ListView):
    """ seguimiento de deudas de un agente"""

    context_object_name = 'agentes'
    template_name = 'administracion/reportes/agentes/list.html'

    def get_queryset(self):
        #recuperamos la consulta de agentes
        return Payment.objects.seguimiento_agentes()


class DeudaByAgentesView(ListView):
    """ Detalle deuda de un agente """

    context_object_name = 'diarios'
    template_name = 'administracion/reportes/agentes/deudas.html'

    def get_context_data(self, **kwargs):
        context = super(DeudaByAgentesView, self).get_context_data(**kwargs)
        context['deuda_total'] = deuda_magazine_agente_total(self.kwargs.get('codigo',0))
        context['agente'] = Vendor.objects.get(cod=self.kwargs.get('codigo',0))
        return context

    def get_queryset(self):
        #recuperamo codigo
        codigo=self.kwargs.get('codigo',0)
        #recuperamos la consulta de agentes
        return deuda_magazine_agente_detalle(codigo)


class EmitirBoletaView(TemplateView):
    """  vista para emitir comprobante de pago """
    template_name = 'administracion/procesos/emitir_boleta.html'


class ListaBoletasEmitidas(ListView):
    """ lista las boletas ya emitidas """
    context_object_name = 'boletas'
    template_name = 'administracion/procesos/lista_boletas.html'

    def get_context_data(self, **kwargs):
        context = super(ListaBoletasEmitidas, self).get_context_data(**kwargs)
        context['form'] = BoletaFilterForm
        return context

    def get_queryset(self):
        q = self.request.GET.get("date_emition", '')
        if q:
            queryset = Boleta.objects.filter(
                date_emition=q,
                anulate=False,
            )
        else:
            queryset = []
        return queryset


class DeleteBoletasEmitida(DeleteView):
    """vista para anular una boleta emitida"""
    model = Boleta
    success_url = reverse_lazy('administracion_app:administracion-proceso_boletas_emitidas')
    template_name = 'administracion/procesos/delete_boleta.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.anulate = True
        self.object.user_modified = self.request.user
        self.object.save()
        #lista de boletas detalle
        detalle_boletas = DetailBoleta.objects.filter(
            boleta__pk=self.object.pk,
        )
        # anulamos cada boleta
        for db in detalle_boletas:
            db.anulate = True
            db.save()
            print 'Detalle boleta anulado'
        #
        success_url = self.get_success_url()

        return HttpResponseRedirect(success_url)


class SearchGuidesView(ListView):
    """ lista guias buscadas por numero de guia"""
    context_object_name = 'guias'
    template_name = 'administracion/reportes/guia/search.html'

    def get_context_data(self, **kwargs):
        context = super(SearchGuidesView, self).get_context_data(**kwargs)
        context['form'] = SearchGuidesForm
        return context

    def get_queryset(self):
        q = self.request.GET.get("kword", '')
        if q:
            queryset = Guide.objects.filter(
                number__icontains=q,
                anulate=False,
            )
        else:
            queryset = Guide.objects.filter(
                anulate=False,
            )[:20]
        return queryset


class HistoryGuidesView(DetailView):
    model = Guide
    template_name = 'administracion/reportes/guia/history.html'

    def get_context_data(self, **kwargs):
        context = super(HistoryGuidesView, self).get_context_data(**kwargs)
        context['historial'] = history_guide(self.get_object().pk)
        return context

class CuadreVentasView(TemplateView):
    template_name = 'administracion/reportes/ventas/por_fecha.html'


class MontosFaltantesView(TemplateView):
    template_name = 'administracion/reportes/faltante/index.html'
