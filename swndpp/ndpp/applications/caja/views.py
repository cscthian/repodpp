# -*- encoding: utf-8 -*-
from datetime import datetime

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

from applications.miscelanea.models import Vendor

from .models import Invoce, Payment
from .forms import LiquidacionDiaForm
from .functions import liquidacion_por_day, resumen_liquidacion


class PaymentRegister(TemplateView):
    """vista para registrar pagos"""
    template_name = 'caja/payment/add.html'


class PaymentDeleteView(DeleteView):
    """vista para anular un pago"""
    template_name = 'caja/payment/anular.html'
    success_url = reverse_lazy('caja_app:add-payment')

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


class LiquidacionDiariaView(ListView):
    context_object_name = 'resultados'
    template_name = 'caja/liquidacion/dia.html'

    def get_context_data(self, **kwargs):
        context = super(LiquidacionDiariaView, self).get_context_data(**kwargs)
        #validamos la fecha
        fecha = self.request.GET.get("date", '')
        if fecha == '':
            fecha = datetime.now().date()
        #
        context['fecha'] = fecha
        context['resumen'] = resumen_liquidacion(fecha)
        context['form'] = LiquidacionDiaForm
        return context

    def get_queryset(self):
        r = self.request.GET.get("date", '')
        queryset = liquidacion_por_day(r)
        return queryset