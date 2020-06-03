# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

#
from .models import PaymentVoucher, Boleta, DetailBoleta


# class PaymentVoucherAdmin(admin.ModelAdmin):
    # list_display = (
    #     'factura',
    #     'codigo_pago',
    #     'date_pago',
    #     'responsabilidad',
    #     'monto_factura',
    #     'diferencia',
    #     'created',
    #     'pk',
    # )
    # search_fields = ('factura',)
    # list_filter = ('responsabilidad','diferencia',)

admin.site.register(PaymentVoucher)
admin.site.register(Boleta)
admin.site.register(DetailBoleta)
