# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from model_utils.models import TimeStampedModel

from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from django.db import models

from applications.recepcion.models import Guide, DetailGuide

from .managers import VoucherManager, NotaCreditoManager


@python_2_unicode_compatible
class Voucher(TimeStampedModel):
    """Comprobantes de pago"""
    TYPE_CHOICES = (
        ('0','Factura electronica'),
        ('1','Otro Comprobante'),
    )

    guide = models.ForeignKey(
        Guide,
        related_name="numero_guia_factura",
        blank=True,
        null=True
    )
    number = models.CharField(
        'numero de factura',
        max_length=20,
    )
    date_emition = models.DateField(
        'fecha de emision',
        blank=True,
        null=True
    )
    date_due = models.DateField(
        'fecha de vencimiento',
        blank=True,
        null=True
    )
    number_interno = models.CharField(
        'codigo interno',
        blank=True,
        max_length=100
    )
    type_voucher = models.CharField(
        'tipo de documento',
        max_length=2,
        choices=TYPE_CHOICES,
        blank=True,
    )
    reference = models.CharField(
        'referencia',
        max_length=20,
        blank=True
    )
    amount = models.DecimalField('monto total',max_digits=10, decimal_places=3)
    anulate = models.BooleanField('anulado',default=False)
    state = models.BooleanField('cancelado',default=False)
    igv = models.BooleanField('con IGV',default=True)
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

    objects = VoucherManager()

    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        ordering = ['-created']

    def __str__(self):
        return self.number


@python_2_unicode_compatible
class DetailVoucher(TimeStampedModel):
    """Comprobantes de pago y guias"""

    voucher = models.ForeignKey(Voucher)
    dettail_guide = models.OneToOneField(
        DetailGuide,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Factura-Guia'
        verbose_name_plural = 'Facturas-Guia'
        ordering = ['-created']

    def __str__(self):
        return str(self.voucher.number)


@python_2_unicode_compatible
class NotaCredito(TimeStampedModel):
    """registramos nota de credito para una factura"""

    voucher = models.ForeignKey(Voucher, related_name="factura_de_nota_credito")
    number = models.CharField(
        'Numero',
        max_length=20,
    )
    date_emition = models.DateField(
        'Fecha de emision',
        blank=True,
        null=True
    )
    reference = models.CharField(
        'referencia',
        max_length=20,
        blank=True
    )
    amount = models.DecimalField('Monto total',max_digits=10, decimal_places=3)
    anulate = models.BooleanField('anulado',default=False)
    state = models.BooleanField('cancelado',default=False)
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="nota_creado_por",
        #editable=False
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="notac_modified",
        blank=True,
        null=True,
        editable=False
    )

    objects = NotaCreditoManager()

    def __str__(self):
        return self.number
