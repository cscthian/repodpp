#from django.db.models import F, FloatField, Sum

from datetime import datetime

from django.conf import settings
from django.db import models


class DetailVoucherManagers(models.Manager):
    def vouchers_by_date(self, date):
        return self.filter(
            anulate=False,
            voucher__date=date,
        )

    def voucher_by_guide(self, guide):
        return self.filter(
            anulate=False,
            guide=guide,
        ).order_by('created')


class VoucherManagers(models.Manager):
    def es_valido(self, numero, date):
        vouchers = self.filter(
            anulate=False,
            number=numero,
        )
        #verificamos si es nueva fecha
        if vouchers.count() !=  vouchers.filter(date=date).count():
            return False
        else:
            return True
