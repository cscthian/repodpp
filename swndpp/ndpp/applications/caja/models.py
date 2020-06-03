# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from model_utils.models import TimeStampedModel
from django.utils.encoding import python_2_unicode_compatible

from django.conf import settings
from django.db import models

from applications.miscelanea.models import Vendor
from applications.recepcion.models import DetailGuide, DetailAsignation

from .managers import PaymentManager, InvoceManager


@python_2_unicode_compatible
class Invoce(TimeStampedModel):
    vendor = models.ForeignKey(Vendor)
    number_operation = models.IntegerField(
        blank=True,
        null=True
    )
    date_operation = models.DateField(
        blank=True,
        null=True
    )
    anulate = models.BooleanField(default=False)
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="invoce_created",
        #editable=False
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="invoce_modified",
        blank=True,
        null=True,
        editable=False
    )
    objects = InvoceManager()

    def __str__(self):
        return str(self.vendor)

    class Meta:
        verbose_name = 'voucher'
        verbose_name_plural = 'vouchers'
        ordering = ['-created']


@python_2_unicode_compatible
class Payment(TimeStampedModel):
    detail_asignation = models.ForeignKey(DetailAsignation)
    invoce = models.ForeignKey(Invoce)
    count_payment = models.PositiveIntegerField(default=0)
    count_return = models.PositiveIntegerField(default=0)
    date = models.DateField()
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=3,
    )
    anulate = models.BooleanField(default=False)
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="payment_created",
        #editable=False
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="payment_modified",
        blank=True,
        null=True,
        editable=False
    )

    objects = PaymentManager()

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        ordering = ['-created']

    def __str__(self):
        return str(self.detail_asignation)


@python_2_unicode_compatible
class Caja(TimeStampedModel):
    amount = models.DecimalField(max_digits=10, decimal_places=3)
    real_amount = models.DecimalField(max_digits=10, decimal_places=3)
    anulate = models.BooleanField(default=False)
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="caja_created",
        #editable=False
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="caja_modified",
        blank=True,
        null=True,
        editable=False
    )
    def __str__(self):
        return str(self.amount)


@python_2_unicode_compatible
class Venta(TimeStampedModel):
    detail_guide = models.ForeignKey(DetailGuide)
    count = models.IntegerField(default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=3)
    anulate = models.BooleanField(default=False)
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="venta_created",
        #editable=False
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="venta_modified",
        blank=True,
        null=True,
        editable=False
    )

    class Meta:
        verbose_name = 'Venta en Tienda'
        verbose_name_plural = 'Ventas en tienda'
        ordering = ['-created']

    def __str__(self):
        return str(self.detail_guide)
