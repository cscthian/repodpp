# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import F, FloatField, Sum, Q
from model_utils.models import TimeStampedModel
from django.utils.encoding import python_2_unicode_compatible

from datetime import datetime, timedelta

from django.conf import settings
from django.db import models

from applications.almacen.entidad.models import Vendor
from applications.almacen.recepcion.models import MagazineDay, DetailGuide
#from applications.caja.pagos.models import Payment

# Create your models here.
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

    def __str__(self):
        return str(self.detail_guide)


class DetailAsignationMananger(models.Manager):
    """ procedimientos para detail asignation """
    def magazine_by_vendor(self, pk_vendor):
        resultado = []
        detail_asignations = self.filter(
            vendor__cod=pk_vendor,
            anulate=False,
            culmined=False,
        ).order_by(
            'asignation__detail_guide__magazine_day__magazine__tipo',
            'created'
        )

        return detail_asignations

    def suma_entregado(self, detail_guide):
        consulta = self.filter(
            anulate=False,
            asignation__anulate=False,
            asignation__detail_guide=detail_guide,
        ).aggregate(suma=Sum('count'))

        if not consulta['suma'] == None:
            return consulta['suma']
        else:
            return 0

    def suma_entregado_guia(self,guide):
        #devuelve la suma total entregada por guia
        consulta = self.filter(
            anulate=False,
            asignation__anulate=False,
            asignation__detail_guide__guide__number=guide,
        ).aggregate(suma=Sum('count'))

        if not consulta['suma'] == None:
            return consulta['suma']
        else:
            return 0

    #candad de asiganciones por dia
    def count_asignation_day(self, fecha):
        consulta = self.filter(
            anulate=False,
            asignation__anulate=False,
            created__date=fecha,
        )
        suma = 0
        for c in consulta:
            suma = suma + c.count

        return suma


    def asignation_by_fecha_vendor(self, fecha1, fecha2):
        #devuelve asignaciones detalle en un rango de fecha
        flat = fecha1 or fecha2

        if flat:
            if fecha1 and fecha2:
                "si se ingreso fecha dos fechas"
                end_date = fecha2
                start_date = fecha1
                #realizamos la consulta
                consulta = self.filter(
                    anulate=False,
                    created__range=(start_date,end_date),
                )
            elif fecha2:
                consulta = self.filter(
                    anulate=False,
                    created__date=fecha2,
                )
            elif fecha1:
                end_date = timezone.now()
                consulta = self.filter(
                    anulate=False,
                    created__range=(fecha1,end_date),
                )

        else:
            end_date = timezone.now()
            start_date = end_date - timedelta(days=7)

            consulta = self.filter(
                anulate=False,
                created__range=(start_date,end_date),
            )

        return consulta


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

    objects = DetailAsignationMananger()

    def __str__(self):
        return str(self.vendor)


#modelo para pautas
@python_2_unicode_compatible
class Pauta(TimeStampedModel):
    """registro de pauta de productos"""
    detail_guide = models.ForeignKey(DetailGuide)
    date = models.DateField()
    enabled = models.BooleanField(default=False)
    anulate = models.BooleanField(default=False)
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="pauta_created",
        #editable=False
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="pauta_modified",
        blank=True,
        null=True,
        editable=False
    )

    def __str__(self):
        return str(self.detail_guide)


#procedimientos para detalle pauta
class DetailPautaMananger(models.Manager):
    def list_ultimos_registros(self, cod,tipo):
        return self.filter(
            vendor__cod=cod,
            pauta__detail_guide__magazine_day__magazine__tipo=tipo,
            asignado=True,
        ).order_by('-modified')[:50]


#modelo que representa un detalle de pauata
@python_2_unicode_compatible
class DetailPauta(TimeStampedModel):
    """Detalle de una pauata producto"""
    vendor = models.ForeignKey(Vendor)
    pauta = models.ForeignKey(Pauta)
    count = models.PositiveIntegerField()
    asignado = models.BooleanField(default=False)
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="pautadetail_created",
        #editable=False
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="pautadetail_modified",
        blank=True,
        null=True,
        editable=False
    )

    objects = DetailPautaMananger()

    def __str__(self):
        return str(self.vendor)


@python_2_unicode_compatible
class Receptors(TimeStampedModel):
    """Tabla que alamacena recpecionista de productos"""
    dni = models.CharField(max_length=8)
    detail_asignation = models.ForeignKey(DetailAsignation)
    anulate = models.BooleanField(default=False)
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="receptors_created",
        #editable=False
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="receptors_modified",
        blank=True,
        null=True,
        editable=False
    )

    def __str__(self):
        return str(self.detail_asignation)
