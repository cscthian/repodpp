# -*- encoding: utf-8 -*-
from django.contrib import admin
from .models import CierreMes

# Register your models here.

class CierreAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'mes',
        'date_start',
        'date_end',
        'venta_neta',
        'ingreso_neto',
        'ingreso_neto_real',
        'venta_neta_real',
    )
    list_filter = ('mes',)

admin.site.register(CierreMes, CierreAdmin)
