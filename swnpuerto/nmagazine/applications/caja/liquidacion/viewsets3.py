# -*- encoding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from datetime import datetime

from .serializers import (
    MovimientosCanillaSerializer,
    GuiaSerializer,
    GudeSerializer,
    LiquidacionProveedorSerializer,
)

from .functions import (
    movimientos_caja,
    liquidacion_guia,
    liquidacion_by_day,
    liquidacion_guia_detalle,
    liquidacion_por_day,
)

class MovimientosCaja(viewsets.ModelViewSet):
    """servicio que lista las deudas de canillas"""
    serializer_class =  MovimientosCanillaSerializer

    def get_queryset(self):
        fecha = self.kwargs['fecha']
        return movimientos_caja(fecha)


class LiquidacionGuia(viewsets.ModelViewSet):
    """servicio que devulete la liquidacion de un proveedor"""
    serializer_class = GuiaSerializer

    def get_queryset(self):
        fecha1 = self.kwargs['fecha1']
        fecha2 = self.kwargs['fecha2']
        prov = self.kwargs['prov']
        return liquidacion_guia(fecha1,fecha2,prov)


class LiquidacionGuiaDetalle(viewsets.ModelViewSet):
    """servicio que devulete la liquidacion de una guia en rango de fecha"""
    serializer_class = GudeSerializer

    def get_queryset(self):
        fecha1 = self.kwargs['fecha1']
        fecha2 = self.kwargs['fecha2']
        return liquidacion_guia_detalle(fecha1,fecha2)


class LiquidacionCaja(viewsets.ModelViewSet):
    """servicio que devulete la liquidacion caja por dia"""
    serializer_class = GuiaSerializer

    def get_queryset(self):
        fecha = self.kwargs['fecha']
        return liquidacion_by_day(fecha)


class LiquidacionProveedorView(viewsets.ModelViewSet):
    """servicio que devulete la liquidacion caja por dia y proveedor"""
    serializer_class = LiquidacionProveedorSerializer

    def get_queryset(self):
        fecha = self.kwargs['fecha']
        print '=============='
        print fecha
        return liquidacion_por_day(fecha)
