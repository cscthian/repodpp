# -*- coding: utf-8 -*-

# django
from datetime import datetime
from django.views.generic import (
    DetailView,
    TemplateView,
    DeleteView,
    CreateView,
    UpdateView,
    ListView
)
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect

from applications.recepcion.models import DetailGuide, Guide
#app miscelanea
from applications.miscelanea.models import Provider, Departamento
#
from applications.recepcion.functions import items_by_guide

from .models import Voucher, NotaCredito, DetailVoucher

from .forms import (
    SearchGuideForm,
    SearchVoucherForm,
    VoucherForm,
    VoucherUpdateForm,
    NotaCreditoForm,
)

from .functions import guias_por_item, facturas_sin_nota

class SearchGuide(ListView):
    '''
        busqueda de guias
    '''
    context_object_name = 'items'
    template_name = 'reportes/guide/list_guide.html'

    def get_context_data(self, **kwargs):
        context = super(SearchGuide, self).get_context_data(**kwargs)
        context['form'] = SearchGuideForm
        return context

    def get_queryset(self):
        q = self.request.GET.get("item", '')
        r = self.request.GET.get("date", '')
        s = self.request.GET.get("provider", '')
        t = self.request.GET.get("departamento", '')
        if (s != ''):
            s = Provider.objects.get(pk=s,disable=False).name
        else:
            s = ''
        #
        if (t != ''):
            t = Departamento.objects.get(pk=t).name
        else:
            t = ''
        #recuperamos guias
        queryset = DetailGuide.objects.search_item_date_guide(q,r,s,t)

        return queryset


class SearchVoucher(ListView):
    '''
        vista para buscar facturas por numero
    '''
    context_object_name = 'facturas'
    template_name = 'reportes/voucher/facturas.html'

    def get_context_data(self, **kwargs):
        context = super(SearchVoucher, self).get_context_data(**kwargs)
        context['form'] = SearchVoucherForm
        return context

    def get_queryset(self):
        q = self.request.GET.get("number", '')
        queryset = Voucher.objects.search_factura(q)
        return queryset


class VoucherCreateView(CreateView,):
    '''registrar nuevo comprobante'''
    form_class = VoucherForm
    success_url = '.'
    template_name = 'reportes/voucher/add.html'

    def form_valid(self, form):
        #guardado desde formulario
        voucher = form.save(commit=False)
        voucher.user_created = self.request.user
        voucher.save()

        return HttpResponseRedirect(
            reverse(
                'reportes_app:update-voucher',
                kwargs={'pk': voucher.pk },
            )
        )


class VoucherUpdateView(UpdateView):
    """ vista para modificar los datos de una factura """

    form_class = VoucherUpdateForm
    model = Voucher
    success_url = '.'
    template_name = 'reportes/voucher/update.html'

    def get_context_data(self, **kwargs):
        context = super(VoucherUpdateView, self).get_context_data(**kwargs)
        context['notas_credito'] = NotaCredito.objects.by_factura(self.get_object())
        return context

    def form_valid(self, form):
        print '****  actualizando datos****'
        #recuperamos el guia
        voucher = form.save(commit=False)
        voucher.user_modified = self.request.user
        voucher.save()
        print '****  se actualizaron los cambios****'
        return super(VoucherUpdateView, self).form_valid(form)



class VoucherDeleteView(DeleteView):
    """Anular Voucher"""
    model = Voucher
    success_url = reverse_lazy('reportes_app:reporte-search_voucher')
    template_name = 'reportes/voucher/delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.anulate = True
        self.object.user_modified = self.request.user
        self.object.save()
        #recuperamos las guias relacionadas a la factura
        guias = DetailVoucher.objects.filter(
            voucher=self.object
        )
        #
        for g in guias:
            g.dettail_guide.facturado = False
            g.dettail_guide.facture = ''
            g.dettail_guide.save()
            g.delete()
            print 'guia sin factura'

        #recuperamos las notas de credito y las eliminamos
        notas = NotaCredito.objects.by_factura(self.object)
        for n in notas:
            n.anulate = True
            n.save()
            print 'Voucher eliminado'
        #
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)



class NotaCreditoCreateView(CreateView):
    '''registrar nueva nota de credito'''
    form_class = NotaCreditoForm
    success_url = '.'
    template_name = 'reportes/nota/add.html'

    def get_context_data(self, **kwargs):
        context = super(NotaCreditoCreateView, self).get_context_data(**kwargs)
        pk_factura=self.kwargs.get('pk',0)
        factura = Voucher.objects.get(pk=pk_factura)
        context['factura'] = factura.number
        return context

    def form_valid(self, form):
        #recuperamos la factura
        pk_factura=self.kwargs.get('pk',0)
        factura = Voucher.objects.get(pk=pk_factura)
        nota = form.save(commit=False)
        nota.voucher = factura
        nota.user_created = self.request.user
        nota.save()

        return HttpResponseRedirect(
            reverse(
                'reportes_app:update-voucher',
                kwargs={'pk': factura.pk },
            )
        )


class NotaCreditoDeleteView(DeleteView):
    """Anular Nota de Credito"""
    model = NotaCredito
    success_url = reverse_lazy('reportes_app:reporte-search_voucher')
    template_name = 'reportes/nota/delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.anulate = True
        self.object.user_modified = self.request.user
        self.object.save()

        return HttpResponseRedirect(
            reverse(
                'reportes_app:update-voucher',
                kwargs={'pk': self.object.voucher.pk },
            )
        )


class FacturaSinCredito(ListView):
    '''
        lista facturas que necesitan una nota de credito
    '''
    context_object_name = 'facturas'
    template_name = 'reportes/voucher/sin_nota_credito.html'

    def get_queryset(self):
        return facturas_sin_nota()
