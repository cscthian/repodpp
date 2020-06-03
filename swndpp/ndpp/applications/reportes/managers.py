from datetime import datetime, timedelta

from django.db.models import F, FloatField, Sum, Q, CharField, Max,ExpressionWrapper,Value as V
from django.db.models.functions import Upper,Coalesce
from django.conf import settings
from django.db import models


class VoucherManager(models.Manager):
    """ procedimientos almacenados para Voucher o Factura """

    def search_factura(self, number):
        """ funcion que busca facturas por numero """
        return self.filter(
            number__icontains=number,
            anulate=False,
        ).order_by('-created')[:20]


    def filter_factura(self, date_start, date_end, number, state):
        """ procedimiento que filtra facturas """
        #verificamos las fechas
        if date_end == '':
            date_end = datetime.now().date()

        if date_start == '':
            date_start = date_end - timedelta(days=7)

        #
        if state == '0':
            consulta = self.filter(
                number__icontains=number,
                date_emition__range=(date_start,date_end),
                anulate=False,
            ).order_by('-date_emition')
        elif state == '1':
            #cerrados
            consulta = self.filter(
                number__icontains=number,
                date_emition__range=(date_start,date_end),
                anulate=False,
                state= True,
            ).order_by('-date_emition')
        else:
            #no cerrados
            consulta = self.filter(
                number__icontains=number,
                date_emition__range=(date_start,date_end),
                anulate=False,
                state = False,
            ).order_by('-date_emition')

        #calculamos el monto
        monto = consulta.aggregate(total=Sum('amount'))
        if not monto['total'] == None:
            total = monto['total']
        else:
            total = 0
        #devolveos diccionario con lista y monto total sumado
        return {'facturas':consulta,'monto':total}


# class DetailVoucherManager(models.Manager):
#     """ procedimientos almacenados para DetailVoucher"""
#
#


class NotaCreditoManager(models.Manager):
    """ procedimientos almacenados para Nota de Credito"""
    def by_factura(self, factura):
        return self.filter(
            voucher=factura,
            anulate=False,
        ).order_by('-created')


    def filter_nota(self, date_start, date_end):
        """ procedimiento que filtra notas de credito en rango de fechas """
        #verificamos las fechas
        if date_end == '':
            date_end = datetime.now().date()

        if date_start == '':
            date_start = date_end - timedelta(days=7)

        #
        consulta = self.filter(
            date_emition__range=(date_start,date_end),
            anulate=False,
        ).order_by('-date_emition')
        #calculamos monto suma de campo amount
        monto = consulta.aggregate(total=Sum('amount_igv'))
        if not monto['total'] == None:
            total = monto['total']
        else:
            total = 0
        #devolveos diccionario con lista y monto total sumado
        return {'notas':consulta,'monto':total}

    def amount_nota_by_facture(self, number_interno):
        """ procedimiento que filtra facturas """
        #filtramos la nostas de creito para el numero iterno
        consulta = self.filter(
            voucher__number_interno=number_interno,
            voucher__anulate=False,
            anulate=False,
        )

        #calculamos el monto
        monto = consulta.aggregate(total=Sum('amount'))
        if not monto['total'] == None:
            total = monto['total']
        else:
            total = 0
        #devolveos diccionario con lista y monto total sumado
        return total
