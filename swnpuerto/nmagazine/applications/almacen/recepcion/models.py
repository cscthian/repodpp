# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from model_utils.models import TimeStampedModel
from django.utils.encoding import python_2_unicode_compatible

from django.utils import timezone

from datetime import datetime, timedelta

from django.conf import settings
from django.db import models

from applications.almacen.entidad.models import Provider

# Create your models here.
class Magazine(TimeStampedModel):
    """tabla para magazine y proucto"""
    MAGAZINE_CHOISES = (
        ('0','Diario'),
        ('1','Producto'),
    )
    name = models.CharField(
        max_length=100
    )
    tipo = models.CharField(
        max_length=2,
        choices=MAGAZINE_CHOISES,
        blank=True,
        null=True,
    )
    provider = models.ForeignKey(Provider)
    description = models.CharField(
        blank=True,
        max_length=100
    )
    day_expiration = models.PositiveIntegerField(default=1)
    sponsor = models.CharField(
        blank=True,
        null=True,
        max_length=7
    )
    code = models.CharField(
        blank=True,
        max_length=15
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

    def __unicode__(self):
        return self.name


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

    def __unicode__(self):
        return u"%s [%s]" % (self.magazine, self.get_day_display())


class GuideManager(models.Manager):
    #funcion que devueve lista de guias en un rango de fechas
    def guias_by_date_range(self, fecha1,fecha2):
        return self.filter(
            anulate=False,
            created__range=(fecha1,fecha2)
        )

    #funcion que devuelve guias culminadas
    def guias_culmined(self, fecha1,fecha2):
        return self.filter(
            anulate=False,
            culmined=True,
            created__range=(fecha1,fecha2)
        )

    #funcion que devuelve guias
    def search_guides(self, numero):
        return self.filter(
            number__icontains=numero,
        ).order_by('-created')

    def search_guides_date(self, date1,date2):
        return self.filter(
            created__range=(date1,date2),
        ).order_by('-created')


class Guide(TimeStampedModel):
    """Guia de remision"""
    ADDRESSEE_CHOICES = (
        ('0','DPP'),
        ('1','MAX CARGO'),
    )

    number = models.CharField(
        max_length=20,
    )
    date = models.DateField()
    number_invoce = models.CharField(
        blank=True,
        max_length=100
    )
    addressee = models.CharField(
        max_length=2,
        choices=ADDRESSEE_CHOICES
    )
    date_emission = models.DateField(
        blank=True,
        null=True
    )
    provider = models.ForeignKey(Provider)
    date_retunr_cargo = models.DateField(
        blank=True,
        null=True
    )
    plazo_return = models.PositiveIntegerField(default=7)
    anulate = models.BooleanField(default=False)
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="guide_created",
        #editable=False
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="guide_modified",
        blank=True,
        null=True,
        editable=False
    )
    culmined = models.BooleanField(default=False)
    asignado = models.BooleanField(default=False)
    returned = models.BooleanField(default=False)

    objects = GuideManager()

    def __str__(self):
        return self.number


class DetailGuideManager(models.Manager):
    def magazine_no_expired(self,tipo):
        #recuperamos la fecha de hoy
        hoy = timezone.now().date()
        #lista de no vencidos
        no_expired = self.filter(
            guide__anulate=False,
            guide__culmined=False,
            anulate=False,
            magazine_day__magazine__tipo__icontains=tipo,
        ).order_by('-created')[:100]
        #inicializamos lista resultado
        #resultado = []
        #for dg in no_expired:
        #    #calculamos los dias de registro
        #    diasregsitro = hoy - dg.guide.date
        #    dias_registro = int(diasregsitro.days)
        #    if dias_registro <= dg.magazine_day.magazine.day_expiration:
        #       resultado.append(dg)

        #return resultado
	return no_expired

    def diarios_by_dia(self,dia):
        #recuperamos la fecha de hoy
        hoy = timezone.now().date()
        end_date = timezone.now()
        start_date = end_date - timedelta(days=30)
        #lista de no vencidos
        detail_magazine = self.filter(
            guide__anulate=False,
            anulate=False,
            magazine_day__magazine__tipo='0',
            magazine_day__day=dia,
            magazine_day__magazine__disable=False,
            created__range=(start_date,end_date),
        ).order_by('-created')
        #inicializamos lista resultado
        resultado = []
        diarios_aux = []
        for dg in detail_magazine:
            #calculamos los dias de registro
            if not dg.magazine_day in diarios_aux:
                resultado.append(dg)
                diarios_aux.append(dg.magazine_day)

        return resultado


    def dias_magazine(self, detail_guide):
        #procedimiento que devuele el tiempo que lleva registrado un magaine day
        guias = self.filter(
            anulate=False,
            pk=detail_guide,
        ).order_by('-created')
        hoy = datetime.now().date()
        diasregsitro = hoy - guias[0].guide.date

        return guias[0].guide.plazo_return - int(diasregsitro.days)


    def magazin_days_date(self, magazine_day, fecha):
        #procedimiento que devuele el tiempo que lleva registrado un magazine
        #repectoa  un dia
        guias = self.filter(
            anulate=False,
            magazine_day__pk=magazine_day,
        ).order_by('-created')
        diasregsitro = fecha - guias[0].created.date()

        return guias[0].guide.plazo_return - int(diasregsitro.days)

    def magazine_count_register(self, fecha):
        #funcion que devuelve cantidad de diarios registrados
        count = 0
        consulta = self.filter(
            anulate=False,
            created__date=fecha,
        )
        for c in consulta:
            count = count + c.count

        return count

    def productos_por_cobrar(self, date):
        lista = self.filter(
            anulate=False,
            culmined=False,
            magazine_day__magazine__tipo='1',
        )
        resultado = []
        date = datetime.strptime(date, '%d-%m-%Y').date()
        for l in lista:
            fecha = l.guide.date + timedelta(days=l.guide.plazo_return-2)
            if fecha == date:
                resultado.append(l)

        return resultado


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
    anulate = models.BooleanField(default=False)
    culmined = models.BooleanField(default=False)
    asignado = models.BooleanField(default=False)
    returned = models.BooleanField(default=False)
    en_reparto = models.BooleanField(default=False)

    objects = DetailGuideManager()

    def __str__(self):
        return str(self.magazine_day)
