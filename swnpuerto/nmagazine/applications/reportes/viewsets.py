# -*- encoding: utf-8 -*-
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from datetime import datetime, timedelta

from .models import CierreMes
from applications.almacen.recepcion.models import Guide, DetailGuide

from .serializers import (
    CierreMesSerializer,
    MagazinRanking,
    VendorRanking,
    HistoriaSerializer,
    CeroSerializer,
    HistoryGuideSerializer,
    CountRealSerializer,
    ResumenGuideSerializer,
)
from .functions import (
    rankin_magazine,
    rankin_vendor,
    vendor_hisotorial,
    canilla_cero,
    history_guide,
    resumen_guia,
)
from applications.administrador.serializers import VentasSerializer
from applications.almacen.recepcion.serializers import GuideListSerializer


class CierreMesViewSet(viewsets.ModelViewSet):
    """servicio que lista cierres de mes"""
    queryset = CierreMes.objects.all().order_by('-created')
    serializer_class = CierreMesSerializer


class VentanetaViewSet(viewsets.ModelViewSet):
    """ lista de 5 ultimas cierres venta neta"""
    serializer_class = VentasSerializer

    def get_queryset(self):
        return CierreMes.objects.ultimas_ventas()


class IngresonetoViewSet(viewsets.ModelViewSet):
    """ lista de 5 ultimos cierres ingreso neto"""
    serializer_class = VentasSerializer

    def get_queryset(self):
        return CierreMes.objects.ultimos_ingresos()


class RankinMagazineSet(viewsets.ModelViewSet):
    """ servicio para ranking de magazins"""
    serializer_class = MagazinRanking

    def get_queryset(self):
        fecha1 = self.kwargs['fecha1']
        fecha2 = self.kwargs['fecha2']
        tipo = self.kwargs['tipo']
        return rankin_magazine(fecha1,fecha2,tipo)


class RankingVendorSet(viewsets.ModelViewSet):
    """servicio para ranking de canillas ultimo mes"""
    serializer_class = VendorRanking

    def get_queryset(self):
        magazine = self.kwargs['pk']
        end_date = datetime.now()
        start_date = end_date - timedelta(days=60)
        return rankin_vendor(start_date, end_date, magazine)


class HistoriaVenderSet(viewsets.ModelViewSet):
    """ mustra la histori desempenio de un canillas"""
    serializer_class = HistoriaSerializer

    def get_queryset(self):
        return vendor_hisotorial()


class CeroVenderSet(viewsets.ModelViewSet):
    """ mustra devoluciones de canillas segun un diario"""
    serializer_class = CeroSerializer

    def get_queryset(self):
        pk_magazine = self.kwargs['pk']
        return canilla_cero(pk_magazine)


class HistoryGuideViewset(viewsets.ModelViewSet):
    """muestra la lista de guias"""
    serializer_class = GuideListSerializer

    def get_queryset(self):
        numero = self.kwargs['numero']
        return Guide.objects.search_guides(numero)


class StateGuideViewset(viewsets.ModelViewSet):
    """muestra la lista de guias en rango de fechas"""
    serializer_class = GuideListSerializer

    def get_queryset(self):
        fecha1 = self.kwargs['date1']
        fecha2 = self.kwargs['date2']
        return Guide.objects.search_guides_date(fecha1,fecha2)


class DetailHistoryGuideViewset(viewsets.ModelViewSet):
    """muestra detalle historico de una guia"""
    serializer_class = HistoryGuideSerializer

    def get_queryset(self):
        detail_guide = self.kwargs['pk']
        return history_guide(detail_guide)


class ResumenReportGuideViewset(viewsets.ModelViewSet):
    """muestra en detalle resumen de guia"""
    serializer_class = ResumenGuideSerializer

    def get_queryset(self):
        date1 = self.kwargs['date1']
        date2 = self.kwargs['date2']
        return resumen_guia(date1,date2)


class RegisterRealCountViewSet(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        print '***********************'
        print request.data
        for data in request.data:
            serializado = CountRealSerializer(data=data)
            if serializado.is_valid():
                #recuperamos el detalle guia
                dg = DetailGuide.objects.get(pk=serializado.validated_data['pk'])
                dg.real_count = serializado.validated_data['count']
                dg.save()
                res = {'respuesta':'Guardado Correctamente','id':'0'}
            else:
                res = {'respuesta':'No se Pudo Guardar','id':'0'}
                print serializado.errors

        return Response(res)
