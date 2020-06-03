from django.db.models import F, FloatField, Sum

from datetime import datetime

from django.conf import settings
from django.db import models


class LostManager(models.Manager):
    def suma_perdidas_module(self,modulo,dg):
        perdidas = self.filter(
            anulate=False,
            close=False,
            module=modulo,
            detail_guide=dg,
        ).aggregate(
            suma_mod=Sum(F('count'))
        )['suma_mod']

        if perdidas == None:
            return 0
        else:
            return perdidas


class BoletaManager(models.Manager):
    def boletas_by_date_range(self,date1,date2):
        #lista boletas en rango de fechas
        fecha1 = datetime.strptime(date1, '%d-%m-%Y').date()
        fecha2 = datetime.strptime(date2, '%d-%m-%Y').date()
        return self.filter(
            created__range=(fecha1,fecha2),
        ).order_by('-created')


class DetailBoletaManager(models.Manager):
    """Procedimientos para Boleta detalle"""

    def existe_magazine(self,magazine_day,date1):
        #lista boletas en rango de fechas
        consulta = self.filter(
            boleta__anulate=False,
            boleta__date_venta=date1,
            anulate=False,
            magazine=magazine_day,
        )
        if consulta.count()>0:
            return True
        else:
            return False

    def existe_magazine2(self,magazine_day,date1,date2):
        #lista boletas en rango de fechas
        consulta = self.filter(
            boleta__anulate=False,
            boleta__date_venta__range=(date1,date2),
            anulate=False,
            magazine=magazine_day,
        )
        if consulta.count()>0:
            return True
        else:
            return False
