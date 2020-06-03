# -*- encoding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from datetime import datetime

#app miscelanea
from applications.miscelanea.models import Provider, Vendor, Departamento
#app caja
from applications.caja.functions import registrar_pagos
#
from applications.caja.models import Invoce

from .models import (
    Magazine,
    MagazineDay,
    Guide,
    DetailGuide,
    Asignation,
    DetailAsignation
)

from .serializers import (
    MagazineSerializer,
    GuideSerializer,
    MagazineDaySerializer,
    ProdSerializer
)


class MagazineListViewSet(viewsets.ModelViewSet):
    """servicio que lista diarios y productos"""
    queryset = Magazine.objects.filter(
        disable=False,
    )
    serializer_class = MagazineSerializer


class MagazineDayViewSet(viewsets.ModelViewSet):
    """servicio que lista magazine_day"""
    queryset = MagazineDay.objects.filter(
        magazine__disable=False,
    )
    serializer_class = MagazineDaySerializer


class GuideAddViewSet(viewsets.ViewSet):
    """servicio que crea una guia"""

    def create(self, request):
        serializado = GuideSerializer(data=request.data)
        if serializado.is_valid():
            #recuperamos datos de Guia
            number = serializado.validated_data['number']
            addressee = serializado.validated_data['addressee']
            proveedor = serializado.validated_data['provider']
            departament = serializado.validated_data['departamento']
            date_emission = serializado.validated_data['date']
            date_cobranza = serializado.validated_data['date_cobranza']
            provider = Provider.objects.get(pk=proveedor)
            departamento = Departamento.objects.get(pk=departament)
            date = datetime.now()

            if not Guide.objects.filter(number=number,anulate=False).exists():
                guide = Guide(
                    number=number,
                    addressee=addressee,
                    date_emission=date_emission,
                    date_cobranza=date_cobranza,
                    provider=provider,
                    departamento=departamento,
                    date=date,
                    user_created=self.request.user,
                )
                guide.save()

                #reuperamos datos de MagazinesDay
                counts = serializado.validated_data['counts']
                prods = serializado.validated_data['prods']
                devolucion = serializado.validated_data['devolucion']
                #variable que acumula el monto total que se aignara a guia
                amount = 0
                #registramos los datos del detalle guia
                for p,c,d in zip(prods,counts,devolucion):
                    magazine_day = MagazineDay.objects.get(
                        pk=p,
                    )
                    guide_detail = DetailGuide(
                        magazine_day=magazine_day,
                        guide=guide,
                        count=c,
                        precio_unitario=magazine_day.precio_venta,
                        precio_tapa=magazine_day.precio_tapa,
                        precio_guia=magazine_day.precio_guia,
                        precio_sunat=magazine_day.precio_guia,
                        user_created=self.request.user,
                    )
                    guide_detail.save()
                    #calculamos el monto
                    amount = amount + guide_detail.precio_guia*guide_detail.count
                    #asignaos a vendedro
                    #recuperamos el agente
                    pk_vendor = serializado.validated_data['agente']
                    vendor = Vendor.objects.get(pk=pk_vendor)
                    #creamos la asignacion
                    asignatio = Asignation(
                        detail_guide=guide_detail,
                        date=datetime.now().date(),
                        user_created=self.request.user,
                    )
                    asignatio.save()
                    #creamos la asignacion detalle
                    detail_asignation = DetailAsignation(
                        vendor=vendor,
                        asignation=asignatio,
                        count=c,
                        precio_venta=guide_detail.precio_unitario,
                        user_created=self.request.user,
                    )
                    detail_asignation.save()
                    #actualizmos asignaicon como asignada
                    guide_detail.asignado=True
                    guide_detail.save()
                    #
                    #registramos la devolucion del producto
                    #creamos factura o comprobante de devolucion
                    factura = Invoce(
                        vendor = vendor,
                        number_operation = '0',
                        date_operation = datetime.now().date(),
                        user_created = self.request.user,
                    )
                    factura.save()
                    #llamamos a la funcion de registro de pagos
                    registrar_pagos(detail_asignation,factura,0,d,self.request.user)

                #remplazamos el monto de la guia
                guide.amount = amount
                guide.save()
                #

                res = {'respuesta':'Guardado Correctamente','id':'0'}
            else:
                res = {'respuesta':'ya existe el numero de guia','id':'1'}
        else:
            print '********************'
            print serializado.errors
            res = {'respuesta':'Verifique Los Datos','id':'1'}
        return Response(res)


class ProdViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        magazine = get_object_or_404(Magazine, pk=pk)
        magazine_day = MagazineDay.objects.get(magazine=magazine)
        serializer = ProdSerializer(magazine_day)
        return Response(serializer.data)
