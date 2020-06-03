# -*- encoding: utf-8 -*-
from django.contrib import admin

# Register your models here.

from .models import Provider, Vendor, Region, Departamento


class ProviderAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'ruc',
        'phone',
        'email',
        'pk',
    )
    search_fields = ('name',)


class VendorAdmin(admin.ModelAdmin):
    list_display = (
        'cod',
        'dni',
        'name',
        'seudonimo',
        'type_vendor',
        'pk',
    )
    search_fields = ('name',)
    list_filter = ('type_vendor',)


class DepartamentoAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'pk',
    )
    search_fields = ('name',)

admin.site.register(Provider, ProviderAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Region)
admin.site.register(Departamento, DepartamentoAdmin)
