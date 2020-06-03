# -*- encoding: utf-8 -*-
from django.contrib import admin

from .models import Payment, Invoce, Venta


class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'detail_asignation',
        'count_payment',
        'count_return',
        'amount',
        'created',
        'anulate',
    )

class InvoceAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'vendor',
        'created',
        'anulate',
    )

# Register your models here.

admin.site.register(Payment, PaymentAdmin)
admin.site.register(Invoce, InvoceAdmin)
admin.site.register(Venta)
