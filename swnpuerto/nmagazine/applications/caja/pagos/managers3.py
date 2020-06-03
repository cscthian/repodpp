from django.db.models import F, FloatField, Sum, Q, CharField, Max,ExpressionWrapper,Value as V
from django.db.models.functions import Upper,Coalesce

from datetime import datetime

from django.conf import settings
from django.db import models


class PaymentManager(models.Manager):
    def suma_payment(self, pk_asignation):
        #funcion que devuleve cantidad de diarios cancelados
        suma = 0
        lista_asignation = self.filter(
            detail_asignation__pk=pk_asignation,
            anulate=False,
        )
        for la in lista_asignation:
            suma = suma + la.count_payment + la.count_return

        return suma

    #consulta que suma os pagos de una detalle asignacion
    def suma_payment2(self, pk_asignation):
        #funcion que devuleve cantidad de diarios cancelados
        suma_total = self.filter(
            detail_asignation__pk=pk_asignation,
            anulate=False,
        ).aggregate(suma=Sum(F('count_payment')+F('count_return')))

        if not suma_total['suma'] == None:
            return suma_total['suma']
        else:
            return 0

    def suma_return(self, pk_asignation):
        #funcion que devuleve cantidad de diarios devueltos
        suma = 0
        lista_asignation = self.filter(
            detail_asignation__pk=pk_asignation,
            anulate=False,
        )
        for la in lista_asignation:
            suma = suma + la.count_return

        return suma

    #suma los pagos de un detalle guia
    def suma_payment_guide(self, detail_guide):
        suma = 0
        lista_asignation = self.filter(
            detail_asignation__asignation__detail_guide=detail_guide,
            anulate=False,
        )
        for la in lista_asignation:
            suma = suma + la.count_payment

        return suma

    #suma las devoluciones de un detalle guia
    def suma_return_guide(self, detail_guide):
        suma = 0
        lista_asignation = self.filter(
            detail_asignation__asignation__detail_guide=detail_guide,
            anulate=False,
        )
        for la in lista_asignation:
            suma = suma + la.count_return

        return suma

    def magazine_by_day(self):
        #recuperamos todo los pagos del dia
        consulta =  self.filter(
            created__date = datetime.now().date(),
            anulate = False,
        )

        magazins = []
        for c in consulta:
            aux = c.detail_asignation.asignation.detail_guide
            if not aux in magazins:
                magazins.append(aux)

        return magazins, consulta

    def by_magazine(self, pk):
        #recuperamos los pagos del dia de un diario
        consulta = self.filter(
            detail_asignation__asignation__detail_guide__magazine_day__pk=pk,
            created__day = datetime.now().day,
            anulate = False
        ).order_by('-created')

        boletas = []
        for c in consulta:
            if not c.invoce in boletas:
                boletas.append(c.invoce)
        #
        return consulta, boletas

    def canillas_by_day(self):
        #recuperamos la lista de canillas por dia
        consulta = self.filter(
            created__day = datetime.now().day,
            anulate = False,
        ).order_by('-created')

        #lista de canillas
        canillas = []
        for c in consulta:
            if not c.detail_asignation.vendor in canillas:
                canillas.append(canillas)


        return canillas

    def payment_by_vendor(self, pk):
        #recuperamos los pagos de un canilla
        consulta = self.filter(
            invoce__pk=pk,
            anulate = False,
        ).order_by('-created')
        #calculamos el monto
        monto = 0
        cantidad = 0
        for c in consulta:
            monto = monto + c.amount
            cantidad = cantidad + c.count_return

        return consulta, monto, cantidad

    def vendor_faltantes(self, vendors):
        #devolvemos lista de canillas faltantes
        consulta = self.filter(
            detail_asignation__culmined=False,
            anulate=False,
            created__day = datetime.now().day,
        )
        #creamos una lista de vendors
        canillas = []
        for c in consulta:
            if not c.invoce.vendor in canillas:
                canillas.append(c.invoce.vendor)

        #creamos lista de faltantes
        faltantes = []
        for v in vendors:
            if not v in canillas:
                faltantes.append(v)

        return faltantes

    def salida_magazine(self, detail_guide):
        #calculamos el stock de un detalle_guia
        consulta = self.filter(
            detail_asignation__asignation__detail_guide__pk=detail_guide,
            detail_asignation__asignation__detail_guide__anulate=False,
            detail_asignation__asignation__detail_guide__culmined=False,
            anulate=False,
        ).aggregate(stock=Sum(F('count_payment')+F('count_return')),devuelto=Sum('count_return'))
        #recorremos la consulta
        if ((consulta['stock'] == None) and (consulta['devuelto'] == None)):
            return 0,0
        else:
            return consulta['stock'], consulta['devuelto']


    def ventas_returned_dia(self,fecha):
        #ventas de un dterminado dia
        return self.filter(
            anulate=False,
            created__date=fecha,
        ).aggregate(Sum('count_return'), Sum('amount'))


    def payment_by_date(self, fecha1, fecha2):
        #pagos en un rango de fechas
        consulta = self.filter(
            anulate=False,
            created__range=(fecha1,fecha2),
        )
        return consulta


    def payment_by_guide(self, guia):
        #pagos en detalle de una guia
        consulta = self.filter(
            anulate=False,
            detail_asignation__asignation__detail_guide__guide=guia,
        ).order_by('detail_asignation__asignation__detail_guide__guide')
        #calculamos totales

        return consulta


    def deuda_by_guide(self, guia, total):
        deuda_guia = self.filter(
            anulate=False,
            detail_asignation__asignation__detail_guide__guide__number=guia,
        ).aggregate(deuda=Sum(F('count_return')+F('count_payment')))
        return total - deuda_guia['deuda']


    def cuadre_caja_guia(self,date):
        consulta = self.filter(
            anulate=False,
            created__date=date,
        ).filter(
            Q(count_return__gt=0) | Q(count_payment__gt=0)
        ).values('detail_asignation__asignation__detail_guide','detail_asignation__asignation__detail_guide__guide__date','detail_asignation__asignation__detail_guide__precio_unitario').annotate(
            guia=Upper('detail_asignation__asignation__detail_guide__guide__number'),
            proveedor=Upper('detail_asignation__asignation__detail_guide__guide__provider__name'),
            devuelto=Sum('count_return'),
            pagado=Sum('count_payment'),
            total=Sum('amount'),
            magazine=Upper('detail_asignation__asignation__detail_guide__magazine_day__magazine__name'),
            dia=Upper('detail_asignation__asignation__detail_guide__magazine_day__day')
        ).order_by('magazine').order_by('guia')

        return consulta


    def list_vendors_day(self, date):
        return self.filter(
            anulate=False,
            created__date=date,
        ).values(
            'detail_asignation__vendor',
            'detail_asignation__vendor__cod',
            'detail_asignation__vendor__name',
            'detail_asignation__vendor__seudonimo',
        ).annotate(
            codigo=Upper('detail_asignation__vendor__cod'),
            monto=Sum('amount'),
        ).order_by('codigo')

    def mov_caja_day(self, date,cod):
        #funcion que devuelve movimienntos de cja
        return self.filter(
            anulate=False,
            date=date,
            detail_asignation__vendor__cod=cod,
        ).annotate(
            codigo=Upper('detail_asignation__vendor__cod'),
            nombre=Upper('detail_asignation__vendor__name'),
            apodo=Upper('detail_asignation__vendor__seudonimo'),
            magazine=Upper('detail_asignation__asignation__detail_guide__magazine_day__magazine__name'),
            dia=Upper('detail_asignation__asignation__detail_guide__magazine_day__day'),
            entregado= F('detail_asignation__count'),
            precio=F('detail_asignation__precio_venta'),
            debe=(F('detail_asignation__count')-(F('count_return')+F('count_payment'))),
            #monto_deuda=ExpressionWrapper((F('detail_asignation__count')-(F('count_return')+F('count_payment')))*F('detail_asignation__precio_venta')), FloatField())
        ).values(
            'created',
            'count_return',
            'count_payment',
            'amount',
            'precio',
            'entregado',
            'codigo',
            'nombre',
            'apodo',
            'debe',
            'magazine',
            'dia',
        )

    def magazine_boleta(self,date):
        return self.filter(
            anulate=False,
            created__date=date,
        ).values(
            'detail_asignation__asignation__detail_guide',
            'detail_asignation__asignation__detail_guide__guide__date',
            'detail_asignation__asignation__created',
            'detail_asignation__asignation__detail_guide__precio_unitario',
            'detail_asignation__asignation__detail_guide__magazine_day__magazine__afecto',
        ).annotate(
            count=Sum('count_payment'),
            amount=Sum('amount'),
            guide=Upper('detail_asignation__asignation__detail_guide__guide__number'),
            vendor=Max('detail_asignation__vendor__cod'),
            vendor_type = Max('detail_asignation__vendor__type_vendor'),
            magazine=Upper('detail_asignation__asignation__detail_guide__magazine_day__magazine__name'),
            dia=Upper('detail_asignation__asignation__detail_guide__magazine_day__day'),
            addressee=Upper('detail_asignation__asignation__detail_guide__guide__addressee')
        ).order_by('magazine')

        return consulta


    def magazine_boleta2(self,date,date2):
        return self.filter(
            anulate=False,
            created__date__range=(date,date2),
        ).values(
            'detail_asignation__asignation__detail_guide',
            'detail_asignation__asignation__detail_guide__guide__date',
            'detail_asignation__asignation__detail_guide__precio_unitario',
            'detail_asignation__asignation__detail_guide__magazine_day__magazine__afecto',
        ).annotate(
            count=Sum('count_payment'),
            amount=Sum('amount'),
            guide=Upper('detail_asignation__asignation__detail_guide__guide__number'),
            vendor=Max('detail_asignation__vendor__cod'),
            vendor_type = Max('detail_asignation__vendor__type_vendor'),
            magazine=Upper('detail_asignation__asignation__detail_guide__magazine_day__magazine__name'),
            dia=Upper('detail_asignation__asignation__detail_guide__magazine_day__day'),
            addressee=Upper('detail_asignation__asignation__detail_guide__guide__addressee')
        ).order_by('magazine')

        return consulta

    def resumen_historia(self, detail_guide):
        #resumen movmeinto detalle guia
        resumen = self.filter(
            anulate=False,
            detail_asignation__asignation__detail_guide__pk=detail_guide,
        ).aggregate(
            count_vendido=Sum((F('count_payment'))),
            count_devuelto=Sum((F('count_return'))),
        )
        if resumen['count_devuelto'] == None:
            resumen['count_devuelto'] = 0
        if resumen['count_vendido'] == None:
            resumen['count_vendido'] = 0

        return resumen

    def historial_detalle_guia(self, detail_guide):
        #lista de movimienntos detalle guia
        return self.filter(
            anulate=False,
            detail_asignation__asignation__detail_guide__pk=detail_guide,
        ).filter(
            Q(count_return__gt=0) | Q(count_payment__gt=0)
        ).values(
            'date'
        ).annotate(
            count_ven=Sum((F('count_payment'))),
            count_dev=Sum((F('count_return'))),
        )

    def deuda_magazine_vendor(self,detail_guide):
        return self.filter(
            anulate=False,
            detail_asignation__asignation__detail_guide__pk=detail_guide,
        ).filter(
            Q(count_return__gt=0) | Q(count_payment__gt=0)
        ).values(
            'detail_asignation__vendor__cod',
            'detail_asignation__vendor__name',
        ).annotate(
            cantidad=Sum(F('detail_asignation__count')-(F('count_return')+F('count_payment'))),
        ).filter(
            cantidad__gt=0,
        )

    def tiene_pagos(self, detail_asignation):
        #verificamos si un detalle asignacion ya tiene pagos
        consulta = self.filter(
            detail_asignation__asignation__pk=detail_asignation,
        )
        if consulta.count() > 0:
            return True
        else:
            return False
