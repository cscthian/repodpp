# -*- encoding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from datetime import datetime

from applications.almacen.entidad.models import Provider, Vendor

from applications.almacen.asignacion.models import Asignation, DetailAsignation

from .models import Magazine, MagazineDay, Guide, DetailGuide
from .serializers import (
    MagazineDaySerializer,
    GuideSerializer,
    MagazineSerializer,
    GuideListSerializer,
    DetailGuideListSerializer,
    DetailGuideSerializer,
    DGcreateSerializer,
    ProdSerializer,
    PorCobrarListSerializer,
    DetailGuideGetSerializer,
)
from .functions import guide_detail


class MagazineViewSet(viewsets.ModelViewSet):
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


class ListDetailGuideViewSet(viewsets.ModelViewSet):
    """servicio que lista detalle guias sin culminar"""
    queryset = DetailGuide.objects.filter(
        guide__culmined=False,
        anulate=False,
        culmined=False,
        discount=False,
    )
    serializer_class = DetailGuideListSerializer


class ListDetailGuideTipoViewSet(viewsets.ModelViewSet):
    """servicio que lista detalle guias por tipo"""
    serializer_class = DetailGuideListSerializer

    def get_queryset(self):
        tipo = self.kwargs['tipo']
        return DetailGuide.objects.filter(
            anulate=False,
            discount=False,
            magazine_day__magazine__tipo=tipo,
        ).order_by('-created')[:1000]


class ProdViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        magazine = get_object_or_404(Magazine, pk=pk)
        magazine_day = MagazineDay.objects.get(magazine=magazine)
        serializer = ProdSerializer(magazine_day)
        return Response(serializer.data)


class GuideListViewSet(viewsets.ModelViewSet):
    """vista que lista guias por fechas"""
    serializer_class = GuideListSerializer

    def get_queryset(self):
        date1 = self.kwargs['date1']
        date2 = self.kwargs['date2']
        queryset = Guide.objects.guias_by_date_range(
            date1,
            date2,
        )
        return queryset


class GuideListCulminedViewSet(viewsets.ModelViewSet):
    """vista que lista guias culmindas en rango de fechas"""
    serializer_class = GuideListSerializer

    def get_queryset(self):
        fecha1 = self.kwargs['date1']
        fecha2 = self.kwargs['date2']
        queryset = Guide.objects.guias_culmined(
            fecha1,
            fecha2,
        )
        return queryset


class DetailGuideListViewSet(viewsets.ModelViewSet):
    """servicio que lista detalle guias por asignar"""
    serializer_class = DetailGuideListSerializer

    def get_queryset(self):
        return DetailGuide.objects.magazine_no_expired('0')

class GuideViewSet(viewsets.ViewSet):
    """servicio que crea una guia"""

    def create(self, request):
        serializado = GuideSerializer(data=request.data)
        if serializado.is_valid():
            #recuperamos datos de Guia
            number = serializado.validated_data['number']
            addressee = serializado.validated_data['addressee']
            number_invoce = serializado.validated_data['invoce']
            proveedor = serializado.validated_data['provider']
            plazo = serializado.validated_data['plazo']
            provider = Provider.objects.get(pk=proveedor)
            date = datetime.now()

            if not Guide.objects.filter(number=number,anulate=False).exists():
                guide = Guide(
                    number=number,
                    number_invoce=number_invoce,
                    addressee=addressee,
                    provider=provider,
                    plazo_return=plazo,
                    date=date,
                    user_created=self.request.user,
                )
                guide.save()

                #reuperamos datos de MagazinesDay
                counts = serializado.validated_data['counts']
                prods = serializado.validated_data['prods']

                for p,c in zip(prods,counts):
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
                    #si se asignara asignamos
                    if serializado.validated_data['asignar'] == True:
                        #recuperamos el agente
                        pk_vendor = serializado.validated_data['agente']
                        print '==========='
                        print pk_vendor
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
                        #actualizmos asignaicon como asihanda
                        guide_detail.asignado=True
                        guide_detail.save()

                res = {'respuesta':'Guardado Correctamente','id':'0'}
            else:
                res = {'respuesta':'ya existe el numero de guia','id':'1'}
        else:
            print '********************'
            print serializado.errors
            res = {'respuesta':'Verifique Los Datos','id':'1'}
        return Response(res)


class DetailGuideViewSet(viewsets.ModelViewSet):
    serializer_class = DetailGuideSerializer

    def get_queryset(self):
        pk_dg = self.kwargs['pk']
        guide = Guide.objects.get(pk=pk_dg)
        queryset = DetailGuide.objects.filter(
            guide=guide,
            anulate=False,
        )
        return queryset


class DGdeleteViewSet(viewsets.ViewSet):

    def destroy(self, request, *args, **kwargs):
        #recuperamos los datos de url
        pk_guia = self.kwargs['guia']
        #recuperamos el detalle de guia
        guide_detail = DetailGuide.objects.get(
            pk=pk_guia,
        )
        print guide_detail
        guide_detail.user_modified = self.request.user
        guide_detail.anulate = True
        #eliminamos la guiadetalle
        guide_detail.save()
        print 'guardado correctamente'

        return Response()


class DGcreateViewSet(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        serializado = DGcreateSerializer(data=request.data)
        if serializado.is_valid():
            #guardamos la nueva guia detalle
            guide = serializado.validated_data['guide']
            #recuperamos guia como objeto
            guide.user_modified=self.request.user
            guide.save()

            magazine_day = serializado.validated_data['magazine_day']
            count = serializado.validated_data['count']

            detail_guide = DetailGuide(
                magazine_day=magazine_day,
                guide=guide,
                count=count,
                precio_unitario=magazine_day.precio_venta,
                precio_tapa=magazine_day.precio_tapa,
                precio_guia=magazine_day.precio_guia,
                precio_sunat=magazine_day.precio_guia,
                user_created=self.request.user,
            )
            detail_guide.save()
        else:
            print serializado.errors

        return Response()


class DetailGuideGetViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        detail_guide = get_object_or_404(DetailGuide, pk=pk)
        serializer = DetailGuideGetSerializer(detail_guide)
        return Response(serializer.data)


class ProductosPorCobrar(viewsets.ModelViewSet):
    serializer_class = PorCobrarListSerializer

    def get_queryset(self):
        date = self.kwargs['date']
        return DetailGuide.objects.productos_por_cobrar(date)
