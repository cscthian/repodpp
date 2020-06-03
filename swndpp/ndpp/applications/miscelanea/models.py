# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from model_utils.models import TimeStampedModel
from django.utils.encoding import python_2_unicode_compatible

from datetime import datetime

from django.conf import settings
from django.db import models


@python_2_unicode_compatible
class Region(TimeStampedModel):
    """tabla de regiones"""
    name = models.CharField(
        'Nombre',
        max_length=300
    )

    class Meta:
        verbose_name = 'Region'
        verbose_name_plural = 'Regiones'
        ordering = ['-created']

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Departamento(TimeStampedModel):
    """tabla departamento de guias"""
    name = models.CharField(
        'Nombre',
        max_length=300
    )

    class Meta:
        verbose_name = 'Departamento Guia'
        verbose_name_plural = 'Departamentos de Guia'
        ordering = ['-created']

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Provider(TimeStampedModel):
    """tabla de provvedores"""
    name = models.CharField(
        'Nombre',
        max_length=100
    )
    ruc = models.CharField(
        max_length=11,
    )
    phone = models.CharField(
        'Telefono',
        blank=True,
        max_length=15
    )
    email = models.EmailField()
    disable = models.BooleanField(default=False)
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="provider_created",
        #editable=False
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="provider_modified",
        blank=True,
        null=True,
        editable=False
    )

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['-created']

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Vendor(TimeStampedModel):
    """tabla canilla o vendedor"""
    VENDOR_CHOICES = (
        ('0', 'Canilla'),
        ('1', 'Agente'),
    )

    cod = models.CharField(
        'Codigo',
        blank=True,
        max_length=8,
        unique=True,
    )
    dni = models.CharField(
        blank=True,
        null=True,
        max_length=8
    )
    name = models.CharField(
        'Nombre',
        blank=True,
        max_length=100
    )
    seudonimo = models.CharField(
        'Seudonimo',
        blank=True,
        max_length=30
    )
    type_vendor = models.CharField(
        'Tipo de Vendedor',
        max_length=2,
        choices=VENDOR_CHOICES,
    )
    line_credit= models.DecimalField(
        'Limite de Credito',
        max_digits=12,
        decimal_places=5
    )
    plazo = models.PositiveIntegerField(default=1)
    disable = models.BooleanField(
        default=False
    )
    region = models.ForeignKey(
        Region,
        blank=True,
        null=True,
    )
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="vendor_created",
        #editable=False
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="vendor_modified",
        blank=True,
        null=True,
        editable=False
    )
    anulate = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Agente'
        verbose_name_plural = 'Agentes'
        ordering = ['-created']

    def __str__(self):
        return self.name
