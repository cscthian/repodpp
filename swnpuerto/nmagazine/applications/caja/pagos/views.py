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

from applications.almacen.entidad.models import Vendor
from applications.almacen.asignacion.models import DetailAsignation
from applications.almacen.recepcion.models import MagazineDay, Guide, DetailGuide

from .models import Payment, Invoce, Venta
from .forms import CajaForm
from .functions import (
    lista_movimientos,
    por_cobrar,
    detalle_movimientos,
    devolucion_movimientos,
    cerrar_guias,
    deuda_detail_guide_vendor
)

# Create your views here.

class CobrosView(TemplateView):
    """vista para realizar proceso de cobro"""
    template_name = 'caja/cobros/cobrar/cobros.html'


class VendorListView(ListView):
    """vista"""
    context_object_name = 'lista_canillas'
    template_name = 'caja/cobros/cobrar/list_anular.html'

    def queryset(self):
        return Payment.objects.magazine_by_day()


class PaymentDeleteView(DeleteView):
    """vista para anular un pago"""
    template_name = 'caja/cobros/cobrar/anular.html'
    success_url = reverse_lazy('pagos_app:pagos-cobrar')

    def get_object(self, queryset=None):
        cod = self.kwargs.get('pk', 0)
        if Vendor.objects.filter(cod=cod).exists():
            obj = Vendor.objects.get(cod=cod)
            return obj
        else:
            obj = Vendor.objects.filter(anulate=False)[0]
            obj.cod = '0'
            obj.name = 'NO EXISTE CANILLA CON ESE CODIGO'
            return obj

    def get_context_data(self, **kwargs):
        context = super(PaymentDeleteView, self).get_context_data(**kwargs)
        cod = self.kwargs.get('pk', 0)
        if Vendor.objects.filter(cod=cod).exists():
            canilla = Vendor.objects.get(cod=cod)
            consulta = Invoce.objects.factura_by_vendor(canilla.pk)
            if len(consulta) > 0:
                pagos, monto, cantidad = Payment.objects.payment_by_vendor(consulta[0].pk)
                context['pagos'] = pagos
                context['monto'] = monto
                context['devuelto'] = cantidad

        else:
            context['monto'] = 'NO EXISTE EL CODIGO'

        return context

    def post(self, request, *args, **kwargs):
        #recuperamos la lista de pagos
        cod = self.kwargs.get('pk', 0)
        canilla = Vendor.objects.get(cod=cod)
        self.object = canilla
        consulta = Invoce.objects.factura_by_vendor(canilla.pk)
        if len(consulta) > 0:
            pagos, monto, cantidad = Payment.objects.payment_by_vendor(consulta[0].pk)
            #acutualizamos cada pago como anulado
            for p in pagos:
                p.anulate = True
                p.user_modified = self.request.user
                p.save()
                #re-abrimos la asignacion
                p.detail_asignation.culmined = False
                p.detail_asignation.save()

            consulta[0].anulate = True
            consulta[0].user_modified = self.request.user
            consulta[0].save()

        success_url = self.get_success_url()

        return HttpResponseRedirect(success_url)


class CuadrarCajaView(TemplateView):
    """vista para cuadre de caja"""
    template_name = 'caja/cobros/cuadrar/cuadrar.html'


class DetalleCuadrarView(DetailView):
    """vista que muestra el detalle de un cuadre de caja"""
    model = MagazineDay
    template_name = 'caja/cobros/cuadrar/detalle.html'

    def get_context_data(self, **kwargs):
        context = super(DetalleCuadrarView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        consulta, boletas = Payment.objects.by_magazine(pk)
        context['list_vendor'] = detalle_movimientos(consulta, boletas)
        context['magazine'] = self.object
        return context


class ConfirmarView(CreateView):
    """vista que confirma un cuadre de caja"""
    form_class = CajaForm
    template_name = 'caja/cobros/cuadrar/confirmar.html'
    success_url = reverse_lazy('users_app:home-caja')

    def get_context_data(self, **kwargs):
        context = super(ConfirmarView, self).get_context_data(**kwargs)
        fecha = datetime.now()
        context['monto'] = Payment.objects.ventas_returned_dia(fecha)['amount__sum']
        return context


    def get_initial(self):
        fecha = datetime.now()
        # recuperamos el objeto equipo
        initial = super(ConfirmarView, self).get_initial()
        initial['real_amount'] = Payment.objects.ventas_returned_dia(fecha)['amount__sum']
        return initial

    def form_valid(self, form):
        fecha = datetime.now()
        monto = Payment.objects.ventas_returned_dia(fecha)['amount__sum']
        conf = form.save(commit=False)
        conf.amount = monto
        conf.user_created = self.request.user
        conf.save()

        #acutualizamos estado de las guias canceladas
        #cerrar_guias()

        return super(ConfirmarView, self).form_valid(form)


class DevolucionListView(TemplateView):
    """vista que cuadra devolucions de magazins"""
    template_name = 'caja/cobros/reportes/devoluciones.html'


class DetalleDevolucion(DetailView):
    """vista que muestra el detalle de un cuadre devolucion"""
    model = MagazineDay
    template_name = 'caja/cobros/reportes/detalle_devolucion.html'

    def get_context_data(self, **kwargs):
        context = super(DetalleDevolucion, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        consulta, boletas = Payment.objects.by_magazine(pk)
        context['list_vendor'] = detalle_movimientos(consulta, boletas)
        context['magazine'] = self.object
        return context


class FaltantesView(ListView):
    """vista que lista canillas falantes de pago"""
    context_object_name = 'list_vendors'
    template_name = 'caja/cobros/reportes/faltantes.html'

    def queryset(self):
        vendors = Vendor.objects.filter(
            anulate = False,
        )
        return Payment.objects.vendor_faltantes(vendors)

class InvoceAnulados(ListView):
    """vista que lista boletas o pagos anulados"""
    context_object_name = 'list_invoce'
    template_name = 'caja/cobros/reportes/anulados.html'

    def queryset(self):
        return Invoce.objects.filter(
            anulate = True,
            created__day = datetime.now().day,
        )


class DetalleAnulado(DetailView):
    """vista que muestra el detalle de una boleta anulada"""
    model = Invoce
    template_name = 'caja/cobros/reportes/detalle_anulados.html'

    def get_context_data(self, **kwargs):
        context = super(DetalleAnulado, self).get_context_data(**kwargs)
        context['list_payment'] = Payment.objects.filter(
            invoce__pk=self.object.pk
        )
        context['boleta'] = self.object
        return context


class CuadrarReporteView(TemplateView):
    """vsta para exportar liquidacion caja"""
    template_name = 'caja/cobros/cuadrar/export.html'


class DevolucionReporteView(TemplateView):
    """vsta para exportar devoluciones caja"""
    template_name = 'caja/cobros/reportes/export_devolucion.html'


class VentaTiendaView(TemplateView):
    """vista para realizar venta de producto en cajas"""
    template_name = 'caja/cobros/cobrar/venta.html'


class VentasListView(ListView):
    """vista que lista ventas emitidas"""
    context_object_name = 'list_ventas'
    template_name = 'caja/cobros/cobrar/list_ventas.html'

    def queryset(self):
        return Venta.objects.filter(
            anulate = False,
            created__day = datetime.now().day,
        ).order_by('-created')


class VentaDeleteView(DeleteView):
    model = Venta
    success_url = reverse_lazy('pagos_app:pagos-tienda')
    template_name = 'caja/cobros/cobrar/venta_delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.anulate = True
        self.object.user_modified = self.request.user
        self.object.save()
        success_url = self.get_success_url()

        return HttpResponseRedirect(success_url)


class GuiasPendientesListView(ListView):
    """vista que lista guias no cerradas en caja"""
    context_object_name = 'guias'
    template_name = 'caja/cobros/reportes/guias_pendientes.html'

    def queryset(self):
        return Guide.objects.filter(
            anulate=False,
            culmined=False,
        ).order_by('created')


class DetalleGuiasPendientesListView(ListView):
    """vista que lista guias no cerradas en caja"""
    context_object_name = 'vendors'
    template_name = 'caja/cobros/reportes/vendors_deudas.html'

    def get_context_data(self, **kwargs):
        context = super(DetalleGuiasPendientesListView, self).get_context_data(**kwargs)
        context['guia'] = Guide.objects.get(
            anulate=False,
            pk=self.kwargs.get('pk', 0)
        ).number
        return context

    def queryset(self):
        guia = Guide.objects.get(
            anulate=False,
            pk=self.kwargs.get('pk', 0)
        ).number
        #
        return deuda_detail_guide_vendor(guia)
