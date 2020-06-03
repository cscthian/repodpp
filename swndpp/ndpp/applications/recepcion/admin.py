# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

# Register your models here.

from .models import (
    Magazine,
    MagazineDay,
    Guide,
    DetailGuide,
    Asignation,
    DetailAsignation
)

class GuideAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'date_emission',
        'addressee',
        'provider',
        'departamento',
        'date_cobranza',
        'culmined',
        'facturado',
        'facture',
        'pk',
    )
    search_fields = ('number','facture',)
    list_filter = ('departamento','culmined','addressee',)


class DetailGuideAdmin(admin.ModelAdmin):
    list_display = (
        'magazine_day',
        'magazine_day__magazine',
        'guide',
        'count',
        'precio_unitario',
        'precio_tapa',
        'precio_guia',
        'pk',
    )
    search_fields = ('guide__number','pk',)
    def magazine_day__magazine(self, obj):
        return str(obj.magazine_day.magazine) + '-'+str(obj.magazine_day.get_day_display())


admin.site.register(Magazine)
admin.site.register(MagazineDay)
admin.site.register(Guide, GuideAdmin)
admin.site.register(DetailGuide, DetailGuideAdmin)
admin.site.register(Asignation)
admin.site.register(DetailAsignation)
