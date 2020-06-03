from datetime import datetime, timedelta

#django libreries
from django.db.models import F, FloatField, Sum, Q, CharField, Max,ExpressionWrapper,Value as V
from django.db.models.functions import Upper,Coalesce
from django.conf import settings
from django.db import models


class DetailGuideManager(models.Manager):
    """ procedimientos almacenados para Detalle de Guia """

    def search_item_date_guide(self, item, date, provider, departamento):
        """ funcion que busca guia por item y fecha """

        consulta = []
        monto_total = 0
        if (date != ''):
            consulta = self.filter(
                anulate=False,
                magazine_day__magazine__name__icontains=item,
                guide__date_emission=date,
                guide__provider__name__icontains=provider,
                guide__departamento__name__icontains=departamento,
            ).order_by('guide__number')

            #calculmos el monto
            consu = consulta.distinct('guide__number')
            #
            for c in consu:
                print '********'
                print c.guide.number
                print c.guide.amount
                monto_total = monto_total + c.guide.amount

            # if not monto_total['suma'] == None:
            #     monto_total = monto_total['suma']
            # else:
            #     monto_total = 0

        return consulta, monto_total

    def filter_guide(self, date_start, date_end, number, state):
        #verificamos las fechas
        if date_end == '':
            date_end = datetime.now().date()

        if date_start == '':
            date_start = date_end - timedelta(days=7)

        #
        if state == '0':
            return self.filter(
                guide__number__icontains=number,
                guide__date_emission__range=(date_start,date_end),
            ).order_by('-guide')
        elif state == '1':
            #cerrados
            return self.filter(
                guide__number__icontains=number,
                guide__date_emission__range=(date_start,date_end),
                guide__culmined = True,
            ).order_by('-created')
        else:
            #no cerrados
            return self.filter(
                guide__number__icontains=number,
                guide__date_emission__range=(date_start,date_end),
                guide__culmined = False,
            ).order_by('-created')


    def items_guide_by_date(self, date):
        """ funcion que devuelve los itemes de una guia por fecha """
        #generamos la consulta de detalle_gui de una guia
        consulta = self.filter(
            guide__date_emission=date,
            anulate=False,
        ).order_by('guide__number')

        return consulta


class DetailAsignationManager(models.Manager):
    """ procedimientos almacenados para Detalle de Asignacion """

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
