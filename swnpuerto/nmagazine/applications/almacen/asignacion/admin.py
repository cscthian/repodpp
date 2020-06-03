# -*- encoding: utf-8 -*-
from django.contrib import admin

from .models import (
    Asignation,
    DetailAsignation,
    Pauta,
    DetailPauta,
    Receptors,
)


class AsignationAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'detail_guide',
        'date',
        'returned',
    )
    list_filter = ('detail_guide',)


class PautaAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'detail_guide',
        'date',
        'anulate',
    )
    list_filter = ('detail_guide',)


class DetailPautaAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'vendor',
        'pauta',
        'count',
        'asignado',
    )
    list_filter = ('pauta',)

# Register your models here.

admin.site.register(Asignation, AsignationAdmin)
admin.site.register(DetailAsignation)
admin.site.register(Pauta, PautaAdmin)
admin.site.register(DetailPauta,DetailPautaAdmin)
admin.site.register(Receptors)
