# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from model_utils.models import TimeStampedModel
from django.utils.encoding import python_2_unicode_compatible

from django.db.models import F, FloatField, Sum, Q, CharField
from django.db.models.functions import Upper

from datetime import datetime

from django.conf import settings
from django.db import models

from applications.almacen.entidad.models import Vendor
from applications.almacen.recepcion.models import DetailGuide
from applications.almacen.asignacion.models import DetailAsignation

from .managers import PaymentManager


class InvoceManager(models.Manager):
    def factura_by_vendor(self, pk_vendor):
        return self.filter(
            vendor__pk=pk_vendor,
            created__date = datetime.now().date(),
            anulate=False,
        ).order_by('-created')


@python_2_unicode_compatible
class Invoce(TimeStampedModel):
    vendor = models.ForeignKey(Vendor)
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


class VentaManager(models.Manager):
    def cuadre_ventas(self,date):
        consulta = self.filter(
            anulate=False,
            created__date=date,
        ).values(
            'detail_guide',
            'detail_guide__guide__date',
            'detail_guide__precio_unitario'
        ).annotate(
            proveedor=Upper('detail_guide__guide__provider__name'),
            vendido=Sum('count'),
            total=Sum('amount'),
            magazine=Upper('detail_guide__magazine_day__magazine__name')
        ).order_by('magazine')

        return consulta

    def guide_vendido(self,dg,date):
        vendido_guia = self.filter(
            anulate=False,
            detail_guide__pk=dg,
            created__date=date,
        ).aggregate(vendido=Sum('count'))
        if not vendido_guia['vendido'] == None:
            return vendido_guia['vendido']
        else:
            return 0


    def ventas_dia(self,date):
        vendido_guia = self.filter(
            anulate=False,
            created__date=date,
        ).aggregate(total=Sum('amount'))
        if not vendido_guia['total'] == None:
            return vendido_guia['total']
        else:
            return 0

    def ventas_detail_guide(self,detail_guide):
        vendido_guia = self.filter(
            anulate=False,
            detail_guide__pk=detail_guide,
        ).aggregate(total=Sum('count'))
        if not vendido_guia['total'] == None:
            return vendido_guia['total']
        else:
            return 0


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

    objects = VentaManager()

    def __str__(self):
        return str(self.detail_guide)
