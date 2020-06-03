# -*- encoding: utf-8 -*-
from django.contrib import admin

from .models import Voucher, DetailVoucher


class VoucherAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'guide',
        'date_emition',
        'date_due',
        'number_interno',
        'type_voucher',
        'reference',
        'amount',
        'pk',
    )
    search_fields = ('number',)
    list_filter = ('date_emition',)


class DetailVoucherAdmin(admin.ModelAdmin):
    list_display = (
        'voucher',
        'item_guia',
        'dettail_guide__pk',
        'pk',
    )
    search_fields = ('voucher__number',)
    def dettail_guide__pk(self, obj):
        return str(obj.dettail_guide.pk)

    def item_guia(self, obj):
        return str(obj.dettail_guide.magazine_day.magazine) + '-'+str(obj.dettail_guide.magazine_day.get_day_display())


admin.site.register(Voucher, VoucherAdmin)
admin.site.register(DetailVoucher, DetailVoucherAdmin)
