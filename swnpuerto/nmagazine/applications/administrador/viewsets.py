# -*- encoding: utf-8 -*-
import decimal

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from datetime import datetime

from .serializers import (
    VentasSerializer,
    NotaItesSerializer,
    BoletaSerializer,
    BoletaSaveSerializer,
    LostSerializer,
    LostListSerializer,
    ReiniciarCuentaSerializer,
    BoletaListSerializer,
)
from .functions import ultimas_ventas, guide_items, items_boleta
from .models import (
    Boleta,
    DetailBoleta,
    LostMagazine,
)

from applications.caja.pagos.models import Payment, Invoce
from applications.almacen.recepcion.models import MagazineDay, DetailGuide


class VentasViewSet(viewsets.ModelViewSet):
    """ lista de 7 ultimas ventas"""
    serializer_class = VentasSerializer

    def get_queryset(self):
        return ultimas_ventas()


class NotaItem(viewsets.ModelViewSet):
    """ lista los items de una guia"""
    serializer_class = NotaItesSerializer

    def get_queryset(self):
        guide = self.kwargs['guide']
        return guide_items(guide)


class ListProdBoleta(viewsets.ModelViewSet):
    """ lista los items a emitir en boleta"""
    serializer_class = BoletaSerializer

    def get_queryset(self):
        date = self.kwargs['date']
        date2 = self.kwargs['date2']
        return items_boleta(date,date2)


class AddBoletaViewSet(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        #recuperamos el primer elemento de la data
        serializ = BoletaSaveSerializer(data=request.data[0])
        if serializ.is_valid():
            monto = serializ.validated_data['total']
            if serializ.validated_data['afecto'] == True:
                igv = (18/decimal.Decimal(100))*decimal.Decimal(monto)
            else:
                igv = 0

            boleta = Boleta(
                number=serializ.validated_data['number'],
                client=serializ.validated_data['client'],
                date_emition=serializ.validated_data['date_emition'],
                date_venta=serializ.validated_data['date_venta'],
                razon_social = serializ.validated_data['addressee'],
                amount=monto,
                igv=igv,
                afecto=serializ.validated_data['afecto'],
                user_created=self.request.user,
            )
            boleta.save()
            print 'boleta registrada'
        else:
            print serializ.errors

        #guardamos los detalles
        for data in request.data:
            #serializamos la data
            serializado = BoletaSaveSerializer(data=data)
            if serializado.is_valid():
                #recuperamos magazine day
                magazine_day = DetailGuide.objects.get(
                    pk=serializado.validated_data['pk']
                ).magazine_day
                #guardamos la dealle boleta
                detail_boleta = DetailBoleta(
                    boleta=boleta,
                    magazine=magazine_day,
                    count=serializado.validated_data['count'],
                    precio_venta=serializado.validated_data['precio_venta'],
                    precio_sunat=serializado.validated_data['precio_sunat'],
                    user_created=self.request.user,
                )
                detail_boleta.save()
                print 'Registrado boleta detalle'
            else:
                print 'no accedio'
                print serializado.errors
        return Response()


class ListBoletaEmitida(viewsets.ModelViewSet):
    """ lista boletas emitidas"""
    serializer_class = BoletaListSerializer

    def get_queryset(self):
        date1 = self.kwargs['date1']
        date2 = self.kwargs['date2']
        return Boleta.objects.boletas_by_date_range(date1,date2)


class AddLostMagazineViewSet(viewsets.ViewSet):
    """servcio que crear un nuevo registro LostMagazine"""

    def create(self, request, *args, **kwargs):
        #guardamos los detalles
        for data in request.data:
            #serializamos la data
            serializado = LostSerializer(data=data)
            if serializado.is_valid():
                #recuperamo el precio venta del diario
                precio_venta = serializado.validated_data['detail_guide'].precio_unitario
                #creamos el objeto LostMagazine
                lost_magazine = LostMagazine(
                    module=serializado.validated_data['module'],
                    detail_guide=serializado.validated_data['detail_guide'],
                    count=serializado.validated_data['count'],
                    precio_venta=precio_venta,
                    description=serializado.validated_data['description'],
                    user_created=self.request.user,
                )
                #guardamos el registro
                lost_magazine.save()
                res = {'respuesta':'Guardado Correctamente','id':'0'}
            else:
                res = {'respuesta':'ya existe el numero de guia','id':'1'}
                print serializado.errors

        return Response(res)


class LostMagazineListViewSet(viewsets.ModelViewSet):
    queryset = LostMagazine.objects.filter(
        anulate=False,
        close=False,
    )
    serializer_class = LostListSerializer


class RinicioCuentaViewSet(viewsets.ViewSet):
    """servicio que reincia la cuenta de un modulo"""

    def create(self, request):
        serializado = ReiniciarCuentaSerializer(data=request.data)
        if serializado.is_valid():
            module = serializado.validated_data['module']

            if module == 'Almacen':
                losts = LostMagazine.objects.filter(
                    anulate=False,
                    close=False,
                    module='0'
                )
            elif module == 'Caja':
                losts = LostMagazine.objects.filter(
                    anulate=False,
                    close=False,
                    module='1'
                )
            else:
                losts = LostMagazine.objects.filter(
                    anulate=False,
                    close=False,
                )

            #guardamos coo cancelado
            for l in losts:
                l.close = True
                l.user_modified = self.request.user
                l.save()

            res = {'respuesta':'Guardado Correctamente','id':'0'}

        else:
            res = {'respuesta':'ya existe el numero de guia','id':'1'}
            print serializado.errors
        return Response(res)
