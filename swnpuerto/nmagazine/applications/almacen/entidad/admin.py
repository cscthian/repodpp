# -*- encoding: utf-8 -*-
from django.contrib import admin
from .models import Provider, Vendor

# Register your models here.

class VendorAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'cod',
        'name',
    )
    list_filter = ('name',)


admin.site.register(Provider)
admin.site.register(Vendor, VendorAdmin)
