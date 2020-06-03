# -*- encoding: utf-8 -*-
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication
)
from rest_framework.permissions import IsAuthenticated

from datetime import datetime
from django.utils import timezone


#application recepcion
from applications.recepcion.models import DetailAsignation, DetailGuide

#
from .serializers import (
    PagoSerializer,
)
from .functions import (
    deuda_magazine_agente,
    registrar_pagos,
)
from .models import Payment, Invoce


class MovimientosGuideViewSet(viewsets.ModelViewSet):
    """ lista de movimientos de una guia por agente """
    serializer_class = PagoSerializer

    def get_queryset(self):
        codigo = self.kwargs['cod']
        return deuda_magazine_agente(codigo)


class PagoscreateViewSet(viewsets.ViewSet):
    """vista para registrar pagos de canillas"""

    def create(self, request, *args, **kwargs):

        ser = PagoSerializer(data=request.data[0])
        if ser.is_valid():
            #recuperamos el canilla
            canilla = detail_asignation = DetailAsignation.objects.get(
                pk=ser.validated_data['pk_asignation']
            ).vendor
            #recgistramos invoce o factura
            factura = Invoce(
                vendor = canilla,
                number_operation = ser.validated_data['number_operation'],
                date_operation = ser.validated_data['date_operation'],
                user_created = self.request.user,
            )
            factura.save()

        print "se ha creado la factura"

        #registramos datos ṕara la factura
        for data in request.data:
            serializado = PagoSerializer(data=data)
            if serializado.is_valid():

                #recuperamos las asiganciones de un diario
                detail_asignation = DetailAsignation.objects.get(
                    pk=serializado.validated_data['pk_asignation']
                )

                #recuperamos valores para actualizar una asignacion
                devuelto = serializado.validated_data['devuelto']
                pagar = serializado.validated_data['pagar']

                #registramos los pagos
                registrar_pagos(detail_asignation,factura, pagar,devuelto,self.request.user)

            else:
                print 'no se logro serializar'
                print serializado.errors

        return Response()
