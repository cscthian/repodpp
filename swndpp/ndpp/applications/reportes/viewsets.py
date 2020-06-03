# -*- encoding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.response import Response

from applications.recepcion.models import DetailGuide, Guide
#
from .models import Voucher, DetailVoucher
#
from .serializers import (
    VoucherGuideSerializer,
    DeleteVoucherGuideSerializer,
    SearchDetailGuideSerializer,
    GuideItemsSerializer
)
#


class VoucherGuideAddViewSet(viewsets.ViewSet):
    """servicio que crea reistra una guia y un factura"""

    def create(self, request):
        for data in request.data:
            serializado = VoucherGuideSerializer(data=data)
            if serializado.is_valid():
                #recuperamos datos de Guia
                voucher = serializado.validated_data['voucher']
                dettail_guide = serializado.validated_data['dettail_guide']
                #guardamos el en detallevoucher si no existe ya
                obj, created = DetailVoucher.objects.update_or_create(
                    voucher=voucher,
                    dettail_guide=dettail_guide,
                    defaults={
                        'voucher': voucher,
                        'dettail_guide': dettail_guide,
                    },
                )
                if created:
                    dettail_guide.facturado = True
                    dettail_guide.date_facture = voucher.date_emition
                    dettail_guide.save()
                    #actualizamos facture
                    dettail_guide.facture = voucher.number_interno
                    dettail_guide.save()
                    #
                    print 'se agrego e detallevoucher guia-facturada'
                else:
                    print 'se actualizo detallevoucher'
            else:
                print '********************'
                print serializado.errors

        return Response()


class VoucherGuideDeleteViewSet(viewsets.ViewSet):
    """servicio que eliminar registra una guia y un factura"""

    def create(self, request):
        serializado = DeleteVoucherGuideSerializer(data=request.data)
        if serializado.is_valid():
            print 'el serializado es valido'
            # recuperamos datos de Guia
            dv = DetailVoucher.objects.get(
                pk=serializado.validated_data['voucher'],
            )
            # actualizamos DetailGuide
            dv.dettail_guide.facturado = False
            dv.dettail_guide.save()
            #actualizamos facture
            dv.dettail_guide.facture = ''
            dv.dettail_guide.save()
            #
            print 'se actualizo estado facturado innactivo'
            dv.delete()
            print 'se eliminado e detallevoucher'
        else:
            print '********************'
            print serializado.errors

        return Response()


class GuideItemsListViewSet(viewsets.ModelViewSet):
    """servicio que lista items de una guia por factura"""

    serializer_class = GuideItemsSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return DetailVoucher.objects.filter(
            voucher__pk=pk
        )


class SearchDetailGuideViewSet(viewsets.ModelViewSet):
    """servicio que lista items de guia buscados por fecha"""

    serializer_class = SearchDetailGuideSerializer

    def get_queryset(self):
        date = self.kwargs['date']
        return DetailGuide.objects.items_guide_by_date(date)
