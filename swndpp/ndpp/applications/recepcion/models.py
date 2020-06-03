# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from model_utils.models import TimeStampedModel

from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from django.db import models

from applications.miscelanea.models import (
    Provider,
    Vendor,
    Departamento
)

#managers
from .managers import DetailGuideManager, DetailAsignationManager

@python_2_unicode_compatible
class Magazine(TimeStampedModel):
    """tabla para magazine y proucto"""
    MAGAZINE_CHOISES = (
        ('0','Diario'),
        ('1','Producto'),
    )
    name = models.CharField(
        'Nombre',
        max_length=100
    )
    tipo = models.CharField(
        max_length=2,
        choices=MAGAZINE_CHOISES,
        blank=True,
        null=True,
    )
    provider = models.ForeignKey(
        Provider,
        related_name="proveedor_diario"
    )
    description = models.CharField(
        'Descripcion',
        blank=True,
        max_length=100
    )
    disable = models.BooleanField(default=False)
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="magazine_created",
        #editable=False
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="magazine_modified",
        blank=True,
        null=True,
        editable=False
    )
    afecto = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-created']

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class MagazineDay(TimeStampedModel):
    """Producto Dia"""
    DAY_CHOICES = (
        ('0','LUNES'),
        ('1','MARTES'),
        ('2','MIERCOLES'),
        ('3','JUEVES'),
        ('4','VIERNES'),
        ('5','SABADO'),
        ('6','DOMINGO'),
        ('7','LUNES-SABADO'),
    )

    magazine = models.ForeignKey(Magazine)
    day = models.CharField(
        max_length=2,
        choices=DAY_CHOICES
    )
    precio_tapa = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )
    precio_guia = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )
    precio_venta = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="magazineday_created",
        #editable=False
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="magazineday_modified",
        blank=True,
        null=True,
        editable=False
    )

    class Meta:
        verbose_name = 'Periodico dia'
        verbose_name_plural = 'Periodicos'
        ordering = ['-created']

    def __str__(self):
        return str(self.magazine.pk)


@python_2_unicode_compatible
class Guide(TimeStampedModel):
    """Guia de remision"""
    ADDRESSEE_CHOICES = (
        ('0','DPP'),
        ('1','MAX CARGO'),
    )

    number = models.CharField(
        'Numero de guia',
        max_length=20,
    )
    date = models.DateField(
        'Fecha de registro',
        blank=True,
        null=True,
        editable=False,
    )
    addressee = models.CharField(
        'Razon Social',
        max_length=2,
        choices=ADDRESSEE_CHOICES
    )
    date_emission = models.DateField(
        'Fecha de Emision',
        blank=True,
        null=True
    )
    provider = models.ForeignKey(Provider, related_name="Proveedor_guia")
    departamento = models.ForeignKey(
        Departamento,
        blank=True,
        null=True,
    )
    date_retunr_cargo = models.DateField(
        blank=True,
        null=True,
        editable=False
    )
    date_cobranza = models.DateField(
        'Fecha de cobranza',
        blank=True,
        null=True
    )
    anulate = models.BooleanField('anulado',default=False)
    pagado = models.BooleanField('pagado',default=False)
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="guia_creado_por",
        #editable=False
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="guide_modified",
        blank=True,
        null=True,
        editable=False
    )
    culmined = models.BooleanField('cerrado',default=False)
    asignado = models.BooleanField('asignado',default=False)
    returned = models.BooleanField('retornado',default=False, editable=False)
    facturado = models.BooleanField('facturado',default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    facture = models.CharField(blank=True, max_length=20)

    class Meta:
        verbose_name = 'Guia'
        verbose_name_plural = 'Guias'
        ordering = ['-created']

    def __str__(self):
        return self.number


@python_2_unicode_compatible
class DetailGuide(TimeStampedModel):
    """guia detalle"""
    magazine_day = models.ForeignKey(MagazineDay)
    guide = models.ForeignKey(Guide)
    count = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )
    precio_tapa = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )
    precio_guia = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )
    precio_sunat = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )
    discount = models.BooleanField(default=False)
    missing = models.PositiveIntegerField(default=0)
    real_count = models.PositiveIntegerField(default=0)
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="detailguide_created",
        #editable=False
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="detailguide_modified",
        blank=True,
        null=True,
        editable=False
    )
    facture = models.CharField(blank=True, max_length=20)
    date_facture = models.DateField(blank=True, null=True)
    anulate = models.BooleanField(default=False)
    culmined = models.BooleanField(default=False)
    facturado = models.BooleanField(default=False)
    asignado = models.BooleanField(default=False)
    returned = models.BooleanField(default=False)
    en_reparto = models.BooleanField(default=False)

    objects = DetailGuideManager()

    class Meta:
        verbose_name = 'Item de Guia'
        verbose_name_plural = 'Items de Guia'
        ordering = ['-created']

    def __str__(self):
        return str(self.magazine_day)


@python_2_unicode_compatible
class Asignation(TimeStampedModel):
    """salida de Diario"""
    detail_guide = models.ForeignKey(DetailGuide)
    date = models.DateField(auto_now_add=True)
    anulate = models.BooleanField(default=False)
    returned = models.BooleanField(default=False)
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="asignation_created",
        #editable=False
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="asignation_modified",
        blank=True,
        null=True,
        editable=False
    )

    class Meta:
        verbose_name = 'Asignacion'
        verbose_name_plural = 'Asignaciones'
        ordering = ['-created']

    def __str__(self):
        return str(self.detail_guide.guide)


@python_2_unicode_compatible
class DetailAsignation(TimeStampedModel):
    """Detalle de una salida"""
    vendor = models.ForeignKey(Vendor)
    asignation = models.ForeignKey(Asignation)
    count = models.PositiveIntegerField()
    precio_venta = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="asignationdetail_created",
        #editable=False
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="asignationdetail_modified",
        blank=True,
        null=True,
        editable=False
    )
    anulate = models.BooleanField(default=False)
    culmined = models.BooleanField(default=False)
    #
    objects = DetailAsignationManager()

    class Meta:
        verbose_name = 'Asignacion canilla'
        verbose_name_plural = 'Asignaciones canillas'
        ordering = ['-created']

    def __str__(self):
        return str(self.vendor)
