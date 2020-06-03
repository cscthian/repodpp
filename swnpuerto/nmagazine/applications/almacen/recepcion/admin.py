# -*- encoding: utf-8 -*-
from django.contrib import admin
from .models import Magazine, MagazineDay, Guide, DetailGuide
# Register your models here.

class MagazineAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'tipo',
        'provider',
        'description',
        'day_expiration',
        'afecto',
    )
    list_filter = ('name',)


class MagazineDayAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'magazine',
        'day',
        'precio_tapa',
        'precio_guia',
        'precio_venta',
    )
    list_filter = ('magazine',)


class GuideAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'number',
        'date',
        'number_invoce',
        'date_emission',
        'provider',
        'date_retunr_cargo',
    )
    list_filter = ('number',)

class DetailGuideAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'magazine_day',
        'guide',
        'count',
        'precio_unitario',
        'precio_tapa',
        'precio_guia',
        'precio_sunat',
        'missing',
        'real_count',
    )
    list_filter = ('magazine_day',)

admin.site.register(Magazine, MagazineAdmin)
admin.site.register(MagazineDay, MagazineDayAdmin)
admin.site.register(Guide, GuideAdmin)
admin.site.register(DetailGuide, DetailGuideAdmin)
