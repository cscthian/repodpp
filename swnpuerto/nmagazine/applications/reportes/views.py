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

from applications.caja.liquidacion.functions import liquidacion_guia_detalle

from .models import CierreMes
from applications.almacen.recepcion.models import Guide, DetailGuide
from applications.caja.pagos.models import Payment

from .forms import CierreForm

class VentaNetaView(TemplateView):
    template_name = 'reportes/ventas/neta.html'


class MargenView(TemplateView):
    template_name = 'reportes/ventas/margen.html'


class CierreCreateView(CreateView):
    """vista que registra cierre de un mes"""
    form_class = CierreForm
    success_url = reverse_lazy('reportes_app:cierre-list')
    template_name = 'reportes/cierre/add.html'

    def form_valid(self, form):
        cierre = form.save(commit=False)
        cierre.user_created = self.request.user
        cierre.user_modified = self.request.user
        dt1 = form.cleaned_data['date_start']
        dt2 = form.cleaned_data['date_end']
        fecha1 = str(dt1.strftime('%d-%m-%Y'))
        fecha2 = str(dt2.strftime('%d-%m-%Y'))
        consulta = liquidacion_guia_detalle(fecha1,fecha2)

        #calculamos ingreso neto real, venta neta real
        ingre_neto = 0
        venta_neta = 0
        #iteramos consulta
        for c in consulta:
            suma_ingres = 0
            suma_venta = 0
            for d in c.detalle:
                suma_ingres = suma_ingres + d.vendido*d.precio_guia
                suma_venta = suma_venta + d.vendido*d.precio_venta
            ingre_neto = ingre_neto + suma_ingres
            venta_neta = venta_neta + suma_venta
        #guardamos los valores

        cierre.venta_neta = venta_neta
        cierre.ingreso_neto = venta_neta - ingre_neto
        cierre.save()
        return super(CierreCreateView, self).form_valid(form)


class CierreMesListView(TemplateView):
    template_name = 'reportes/cierre/list.html'


class CierreMesDeleteView(DeleteView):
    model = CierreMes
    success_url = reverse_lazy('reportes_app:cierre-list')
    template_name = 'reportes/cierre/delete.html'


class DiariosReport(TemplateView):
    template_name = 'reportes/diarios/report.html'


class ProductReport(TemplateView):
    template_name = 'reportes/productos/report.html'


class VendorReport(TemplateView):
    template_name = 'reportes/canillas/report.html'


class VendorTopeReport(TemplateView):
    template_name = 'reportes/canillas/tope.html'


class VendorHistoriaReport(TemplateView):
    template_name = 'reportes/canillas/historial.html'


class VendorCeroReport(TemplateView):
    template_name = 'reportes/canillas/cero.html'


class MagazineMissingReport(TemplateView):
    template_name = 'reportes/almacen/perdidas.html'


class ControlGuidesReport(TemplateView):
    template_name = 'admin/control/guides_culmined.html'


class GuidesReport(TemplateView):
    template_name = 'reportes/almacen/reporte_guias.html'


class GuidesItemReport(DetailView):
    model = Guide
    template_name = 'reportes/almacen/items_guias.html'


class GuidesItemDetalleReport(DetailView):
    model = DetailGuide
    template_name = 'reportes/almacen/items_detalle.html'

    def get_context_data(self, **kwargs):
        context = super(GuidesItemDetalleReport, self).get_context_data(**kwargs)
        context['deudas'] = Payment.objects.deuda_magazine_vendor(
            self.get_object().pk,
        )
        return context


class GuideEstadoReport(TemplateView):
    template_name = 'reportes/almacen/estado_guias.html'


class GuideResumenReport(TemplateView):
    template_name = 'reportes/almacen/resumen_guias.html'
