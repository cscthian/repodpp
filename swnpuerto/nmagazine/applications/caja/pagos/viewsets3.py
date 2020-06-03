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

from .serializers import (
    PagoSerializer,
    CuadrarCajaSerializer,
    ProdVentaSerializer,
    RegisterVentaSerializer,
)
from .functions import (
    magazine_pago_canilla,
    registrar_pagos,
    lista_movimientos,
    deuda_magazine_canilla,
    listar_productos_venta,
)
from .models import Payment, Invoce, Venta

from applications.almacen.entidad.models import Vendor
from applications.almacen.asignacion.models import Asignation, DetailAsignation
from applications.almacen.recepcion.models import DetailGuide


class MovimientosViewSet(viewsets.ModelViewSet):
    """ lista de movimientos de un vendor """
    serializer_class = PagoSerializer

    def get_queryset(self):
        type_user = self.request.user.type_user
        codigo = self.kwargs['pk']
        return deuda_magazine_canilla(codigo,type_user)


class PagoscreateViewSet(viewsets.ViewSet):
    """vista para registrar pagos de canillas"""

    def create(self, request, *args, **kwargs):
        #recuperamos el canilla
        pk_canilla = self.kwargs['pk']
        canilla = Vendor.objects.get(cod=pk_canilla)

        #creamoe la Factura
        factura = Invoce(
            vendor = canilla,
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


class CuadrarCajaViewSet(viewsets.ModelViewSet):
    """ servicio para reporte liquidacion de caja """
    serializer_class = CuadrarCajaSerializer

    def get_queryset(self):
        resultado, monto  = lista_movimientos()
        return resultado


class ProdVentaViewSet(viewsets.ModelViewSet):
    """ lista productos en venta """
    serializer_class = ProdVentaSerializer

    def get_queryset(self):
        return listar_productos_venta()


class VentacreateViewSet(viewsets.ViewSet):
    """vista para registrar ventas en caja"""

    def create(self, request, *args, **kwargs):
        #recuperamos cada producto vendido
        for data in request.data:
            serializado = RegisterVentaSerializer(data=data)
            if serializado.is_valid():
                #recuperamos el diario
                detail_guide = DetailGuide.objects.get(
                    pk=serializado.validated_data['pk']
                )
                #creamos el objeto venta
                venta = Venta(
                    detail_guide=detail_guide,
                    count=serializado.validated_data['count'],
                    amount=serializado.validated_data['count']*detail_guide.precio_unitario,
                    user_created=self.request.user,
                )
                venta.save()
                print 'Venta Registrada'
                #res = {'id':'0','msj':'Guardado Correctamente'}

            else:
                #res = {'id':'1','msj':'Los Datos no son Correctos'}
                print 'Erro al registrar Venta'
                print serializado.errors

        return Response()
