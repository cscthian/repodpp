# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from model_utils.models import TimeStampedModel
from django.utils.encoding import python_2_unicode_compatible

from datetime import datetime

from django.conf import settings

from django.db import models

from applications.almacen.recepcion.models import MagazineDay,DetailGuide

from .managers import LostManager, BoletaManager, DetailBoletaManager


# Create your models here.
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

    objects = BoletaManager()

    def __unicode__(self):
        return u'%s'%(self.client)


class DetailBoleta(TimeStampedModel):
    """almacena boletas emitidas"""
    boleta = models.ForeignKey(Boleta)
    magazine = models.ForeignKey(MagazineDay)
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

    objects = DetailBoletaManager()


    def __unicode__(self):
        return u'%s'%(str(self.magazine))


class LostMagazine(TimeStampedModel):
    """Registra prouctos perdidos por modulo y Detalle Guia"""
    MODULE_CHOISES = (
        ('0','Almacen'),
        ('1','Caja'),
        ('2','Trasporte'),
    )
    module = models.CharField(
        max_length=2,
        choices=MODULE_CHOISES,
    )
    detail_guide = models.ForeignKey(
        DetailGuide,
        blank=True,
        null=True
    )
    count = models.PositiveIntegerField(
        blank=True,
        null=True
    )
    precio_venta = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )
    description = models.TextField(blank=True)
    close = models.BooleanField(default=False)
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="lost_created",
        #editable=False
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="lost_modified",
        blank=True,
        null=True,
        editable=False
    )
    anulate = models.BooleanField(default=False)
    objects = LostManager()


    def __unicode__(self):
        return u'%s'%(str(self.module))
