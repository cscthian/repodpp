from django.db.models import F, FloatField, Sum, Q, CharField, Max,ExpressionWrapper,Value as V
from django.db.models.functions import Upper,Coalesce

from datetime import datetime

from django.conf import settings
from django.db import models


class InvoceManager(models.Manager):
    def factura_by_vendor(self, pk_vendor):
        return self.filter(
            vendor__pk=pk_vendor,
            created__date = datetime.now().date(),
            anulate=False,
        ).order_by('-created')


class PaymentManager(models.Manager):

    #consulta que suma os pagos de una detalle asignacion
    def suma_payment(self, pk_asignation):
        #funcion que devuleve cantidad de diarios cancelados
        suma_total = self.filter(
            detail_asignation__pk=pk_asignation,
            anulate=False,
        ).aggregate(suma=Sum(F('count_payment')+F('count_return')))

        if not suma_total['suma'] == None:
            return suma_total['suma']
        else:
            return 0

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

    def cuadre_caja_guia(self,date):
        consulta = self.filter(
            anulate=False,
            created__date=date,
        ).filter(
            Q(count_return__gt=0) | Q(count_payment__gt=0)
        ).values(
            'detail_asignation__asignation__detail_guide',
            'detail_asignation__asignation__detail_guide__guide__date',
            'detail_asignation__asignation__detail_guide__precio_unitario',
            'detail_asignation__asignation__detail_guide__count'
        ).annotate(
            guia=Upper('detail_asignation__asignation__detail_guide__guide__number'),
            proveedor=Upper('detail_asignation__asignation__detail_guide__guide__provider__name'),
            devuelto=Sum('count_return'),
            pagado=Sum('count_payment'),
            total=Sum('amount'),
            magazine=Upper('detail_asignation__asignation__detail_guide__magazine_day__magazine__name'),
            dia=Upper('detail_asignation__asignation__detail_guide__magazine_day__day')
        ).order_by('magazine').order_by('guia')

        return consulta

    # funcion que devuelve la ventas en un rango de tiempo
    def cuadre_ventas_date(self,date1, date2):
        consulta = self.filter(
            anulate=False,
            created__date__range=(date1, date2),
        ).filter(
            Q(count_return__gt=0) | Q(count_payment__gt=0)
        ).values(
            'detail_asignation__asignation__detail_guide',
            'detail_asignation__asignation__detail_guide__guide__date',
            'detail_asignation__asignation__detail_guide__precio_unitario',
            'detail_asignation__asignation__detail_guide__count'
        ).annotate(
            guia=Upper('detail_asignation__asignation__detail_guide__guide__number'),
            proveedor=Upper('detail_asignation__asignation__detail_guide__guide__provider__name'),
            devuelto=Sum('count_return'),
            pagado=Sum('count_payment'),
            total=Sum('amount'),
            magazine=Upper('detail_asignation__asignation__detail_guide__magazine_day__magazine__name'),
            dia=Upper('detail_asignation__asignation__detail_guide__magazine_day__day')
        ).order_by('detail_asignation__asignation__detail_guide__guide__date')

        return consulta

    #
    def movimientos_by_guia_by_departamento(self, provider, departamento, razon_social):
        """ devuelve detalle de movimientos de guias """

        consulta = self.filter(
            anulate=False,
            detail_asignation__asignation__detail_guide__anulate=False,
            detail_asignation__asignation__detail_guide__guide__pagado=False,
            detail_asignation__asignation__detail_guide__guide__addressee=razon_social,
            detail_asignation__asignation__detail_guide__guide__departamento__pk=departamento,
            detail_asignation__asignation__detail_guide__guide__provider__pk=provider,
        ).values(
            'detail_asignation__asignation__detail_guide',
            'detail_asignation__asignation__detail_guide__guide__date_emission',
            'detail_asignation__asignation__detail_guide__precio_guia',
            'detail_asignation__asignation__detail_guide__count'
        ).annotate(
            guia=Upper('detail_asignation__asignation__detail_guide__guide__number'),
            proveedor=Upper('detail_asignation__asignation__detail_guide__guide__provider__name'),
            departamento=Upper('detail_asignation__asignation__detail_guide__guide__departamento__name'),
            cantidad = Max('detail_asignation__asignation__detail_guide__count'),
            precio = Max('detail_asignation__asignation__detail_guide__precio_guia'),
            devuelto=Sum('count_return'),
            pagado=Sum('count_payment'),
            magazine=Upper('detail_asignation__asignation__detail_guide__magazine_day__magazine__name'),
            dia=Upper('detail_asignation__asignation__detail_guide__magazine_day__day'),
        ).order_by('detail_asignation__asignation__detail_guide__guide__date_emission','guia')

        return consulta

    #
    def movimientos_by_guia_by_departamento_facturado(self, provider, departamento, razon_social, date):
        """ devuelve detalle de movimientos de guias facturadas """

        consulta = self.filter(
            anulate=False,
            detail_asignation__asignation__detail_guide__anulate=False,
            detail_asignation__asignation__detail_guide__guide__pagado=False,
            detail_asignation__asignation__detail_guide__facturado=True,
            detail_asignation__asignation__detail_guide__guide__date_emission=date,
            detail_asignation__asignation__detail_guide__guide__addressee=razon_social,
            detail_asignation__asignation__detail_guide__guide__departamento__pk=departamento,
            detail_asignation__asignation__detail_guide__guide__provider__pk=provider,
        ).values(
            'detail_asignation__asignation__detail_guide',
            'detail_asignation__asignation__detail_guide__guide__date_emission',
            'detail_asignation__asignation__detail_guide__date_facture',
            'detail_asignation__asignation__detail_guide__precio_guia',
            'detail_asignation__asignation__detail_guide__count'
        ).annotate(
            facture=Upper('detail_asignation__asignation__detail_guide__facture'),
            guia=Upper('detail_asignation__asignation__detail_guide__guide__number'),
            proveedor=Upper('detail_asignation__asignation__detail_guide__guide__provider__name'),
            departamento=Upper('detail_asignation__asignation__detail_guide__guide__departamento__name'),
            cantidad = Max('detail_asignation__asignation__detail_guide__count'),
            precio = Max('detail_asignation__asignation__detail_guide__precio_guia'),
            devuelto=Sum('count_return'),
            pagado=Sum('count_payment'),
            magazine=Upper('detail_asignation__asignation__detail_guide__magazine_day__magazine__name'),
            dia=Upper('detail_asignation__asignation__detail_guide__magazine_day__day'),
        ).order_by('facture')

        return consulta


    def ventas_by_guide(self, guide):
        """ devuelve ventas de una guia"""

        consulta = self.filter(
            anulate=False,
            detail_asignation__asignation__detail_guide__anulate=False,
            detail_asignation__asignation__detail_guide__guide=guide,
        ).filter(
            Q(count_return__gt=0) | Q(count_payment__gt=0)
        ).values(
            'detail_asignation__asignation__detail_guide',
            'detail_asignation__asignation__detail_guide__guide__date_emission',
            'detail_asignation__asignation__detail_guide__precio_unitario',
            'detail_asignation__asignation__detail_guide__count'
        ).annotate(
            guia=Upper('detail_asignation__asignation__detail_guide__guide__number'),
            facture=Upper('detail_asignation__asignation__detail_guide__guide__facture'),
            proveedor=Upper('detail_asignation__asignation__detail_guide__guide__provider__name'),
            departamento=Upper('detail_asignation__asignation__detail_guide__guide__departamento__name'),
            devuelto=Sum('count_return'),
            magazine=Upper('detail_asignation__asignation__detail_guide__magazine_day__magazine__name'),
            dia=Upper('detail_asignation__asignation__detail_guide__magazine_day__day'),
            subtotal=Sum(
                (F('detail_asignation__asignation__detail_guide__count')*F('detail_asignation__asignation__detail_guide__precio_unitario'))-(F('count_return')*F('detail_asignation__asignation__detail_guide__precio_unitario')),output_field=FloatField()
            ),
        ).order_by('facture')

        monto_calculado = consulta.aggregate(
            monto=Sum('subtotal')
        )

        if monto_calculado['monto'] != None:
            total = monto_calculado['monto']
        else:
            total = 0

        return consulta, total

    #
    def ventas_by_vocher_factura(self, number_interno):
        """ devuelve ventas de una factura registrada"""

        consulta = self.filter(
            anulate=False,
            detail_asignation__asignation__detail_guide__anulate=False,
            detail_asignation__asignation__detail_guide__facturado=True,
            detail_asignation__asignation__detail_guide__facture=number_interno,
        ).filter(
            Q(count_return__gt=0) | Q(count_payment__gt=0)
        )

        total = 0
        for c in consulta:
            total = total + c.amount

        return total

    #
    def seguimiento_agentes(self):
        """ devuelve seguimientos de agentes """
        #recuperamos fechas
        date = datetime.now().date()
        print '**************+'
        print date
        #
        consulta = self.filter(
            anulate=False,
            detail_asignation__asignation__detail_guide__anulate=False,
            detail_asignation__asignation__detail_guide__guide__pagado=False,
        ).filter(
            Q(count_return__gt=0) | Q(count_payment__gt=0)
        ).values(
            'detail_asignation__vendor__cod'
        ).annotate(
            name=Upper('detail_asignation__vendor__name'),
            total=Sum(
                ((F('detail_asignation__count')-F('count_return')-F('count_payment'))*F('detail_asignation__asignation__detail_guide__precio_unitario')),output_field=FloatField()
            ),
        ).order_by('detail_asignation__vendor__cod')

        return consulta

    #
    def magazine_boleta(self,date,rs,dep):
        return self.filter(
            anulate=False,
            created__date=date,
            detail_asignation__asignation__detail_guide__guide__addressee=rs,
            detail_asignation__asignation__detail_guide__guide__departamento__pk=dep,
        ).values(
            'detail_asignation__asignation__detail_guide',
            'detail_asignation__asignation__detail_guide__guide__date_emission',
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

    #
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
