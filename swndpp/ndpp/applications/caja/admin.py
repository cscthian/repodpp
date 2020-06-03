# -*- encoding: utf-8 -*-
from django.contrib import admin

# Register your models here.

from .models import Invoce, Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'detail_asignation',
        'invoce',
        'count_payment',
        'count_return',
        'date',
        'amount',
        'created',
        'pk',
    )
    list_filter = ('date',)

admin.site.register(Invoce)
admin.site.register(Payment, PaymentAdmin)
