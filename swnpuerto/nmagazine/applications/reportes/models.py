# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from model_utils.models import TimeStampedModel
from django.utils.encoding import python_2_unicode_compatible

from datetime import datetime

from django.conf import settings
from django.db.models import F, FloatField, Sum
from django.db import models

from applications.administrador.functions import VentaDia


class CierreMananger(models.Manager):
    #funcion que devuleve las 5 ultimas ventas
    def ultimas_ventas(self):
        consulta = self.all().order_by('created')[:5]
        resultado = []
        for c in consulta:
            ventas = VentaDia()
            ventas.label = c.get_mes_display
            ventas.value = c.venta_neta_real
            resultado.append(ventas)
        return resultado

    def ultimos_ingresos(self):
        consulta = self.all().order_by('created')[:5]
        resultado = []
        for c in consulta:
            ventas = VentaDia()
            ventas.label = c.get_mes_display
            ventas.value = c.ingreso_neto_real
            resultado.append(ventas)
        return resultado



@python_2_unicode_compatible
class CierreMes(TimeStampedModel):
    """tabla que reistra cierre de mes"""
    MES_CHOICES = (
            ('1', 'Enero'),
            ('2', 'Febrero'),
            ('3', 'Marzo'),
            ('4', 'Abril'),
            ('5', 'Mayo'),
            ('6', 'Junio'),
            ('7', 'Julio'),
            ('8', 'Agosto'),
            ('9', 'Setiembre'),
            ('10', 'Octubre'),
            ('11', 'Novimbre'),
            ('12', 'Diciembre'),
    )

    mes = models.CharField(
        max_length=2,
        choices=MES_CHOICES,
    )
    date_start = models.DateField(
        blank=True,
        null=True,
    )
    date_end = models.DateField(
        blank=True,
        null=True,
    )
    venta_neta = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        default=0
    )
    ingreso_neto = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        default=0,
    )
    venta_neta_real = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )
    ingreso_neto_real = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )
    igv = models.DecimalField(
        max_digits=3,
        decimal_places=3,
        default=0.18,
    )
    anulate = models.BooleanField(default=False)
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="cierre_created",
        #editable=False
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="cierre_modified",
        blank=True,
        null=True,
        editable=False
    )

    objects = CierreMananger()

    def __str__(self):
        return self.mes
