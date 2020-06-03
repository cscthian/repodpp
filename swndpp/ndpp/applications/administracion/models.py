# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from model_utils.models import TimeStampedModel

from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from django.db import models

#app recepcion
from applications.recepcion.models import DetailGuide
#
from applications.reportes.models import Voucher


@python_2_unicode_compatible
class PaymentVoucher(TimeStampedModel):
    """Pagos de Factura"""

    RESPONSABILITY_CHOICES = (
        ('0','---'),
        ('1','Admin'),
        ('2','Almacen'),
        ('3','Caja'),
        ('4','Otros'),
    )

    factura = models.ForeignKey(
        Voucher,
        related_name="factura_pago",
    )
    codigo_pago = models.CharField(
        'Codigo de Transaccion',
        max_length=30,
    )
    date_pago = models.DateField(
        'fecha de pago',
        blank=True,
        null=True
    )
    responsabilidad = models.CharField(
        'Responsabilidad',
        max_length=2,
        choices=RESPONSABILITY_CHOICES
    )
    monto_real = models.DecimalField('monto real',max_digits=10, decimal_places=3)
    monto_factura = models.DecimalField('monto Factura',max_digits=10, decimal_places=3)
    diferencia = models.BooleanField(default=False)
    #saldado = models.BooleanField(default=True)
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="voucher_pago_created",
        #editable=False
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="voucher_pago_modified",
        blank=True,
        null=True,
        editable=False
    )

    class Meta:
        verbose_name = 'Pago de Facturas'
        verbose_name_plural = 'Pagos de Facturas'
        ordering = ['-created']

    def __str__(self):
        return str(self.factura.number)


@python_2_unicode_compatible
class Boleta(TimeStampedModel):
    """almacena boletas emitidas"""
    RS_CHOICES = (
        ('0','DPP'),
        ('1','MAX CARGO'),
    )

    number = models.CharField(
        blank=True,
        max_length=20
    )
    client = models.CharField(
        blank=True,
        max_length=200
    )
    date_emition = models.DateField(
        blank=True,
        null=True,
    )
    date_venta = models.DateField(
        blank=True,
        null=True,
    )
    razon_social = models.CharField(
        max_length=2,
        choices=RS_CHOICES
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )
    igv = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )
    afecto = models.BooleanField(default=True)
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="boleta_created",
        #editable=False
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="boleta_modified",
        blank=True,
        null=True,
        editable=False
    )
    anulate = models.BooleanField(default=False)

    #objects = BoletaManager()

    def __str__(self):
        return str(self.number)


@python_2_unicode_compatible
class DetailBoleta(TimeStampedModel):
    """almacena boletas emitidas"""
    boleta = models.ForeignKey(Boleta)
    detail_guide = models.ForeignKey(DetailGuide)
    count = models.PositiveIntegerField(
        blank=True,
        null=True
    )
    precio_venta = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )
    precio_sunat = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="detailboleta_created",
        #editable=False
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="detailboleta_modified",
        blank=True,
        null=True,
        editable=False
    )
    anulate = models.BooleanField(default=False)

    #objects = DetailBoletaManager()


    def __str__(self):
        return str(self.boleta.number)
