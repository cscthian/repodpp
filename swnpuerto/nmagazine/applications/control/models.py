# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from model_utils.models import TimeStampedModel
from django.utils.encoding import python_2_unicode_compatible

from datetime import datetime

from django.conf import settings

from django.db import models

from applications.almacen.recepcion.models import Guide

from .managers import DetailVoucherManagers, VoucherManagers


@python_2_unicode_compatible
class Voucher(TimeStampedModel):
    """almacena voucher de deposito de pago"""
    number = models.CharField(
        max_length=15
    )
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="voucher_created",
        #editable=False
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="voucher_modified",
        blank=True,
        null=True,
        editable=False
    )
    date = models.DateField(
        blank=True,
        null=True,
    )
    anulate = models.BooleanField(default=False)
    objects = VoucherManagers()

    def __str__(self):
        return self.number


@python_2_unicode_compatible
class DetailVoucher(TimeStampedModel):
    """alamcena voucher guia"""
    voucher = models.ForeignKey(Voucher)
    guide = models.ForeignKey(Guide)
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="voucher_detail_created",
        #editable=False
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="voucher_detail_modified",
        blank=True,
        null=True,
        editable=False
    )
    anulate = models.BooleanField(default=False)

    objects = DetailVoucherManagers()

    def __str__(self):
        return str(self.voucher) + '-'+str(self.guide)
