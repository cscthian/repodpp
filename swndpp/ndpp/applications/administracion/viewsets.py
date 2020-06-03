# -*- encoding: utf-8 -*-
import decimal
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
    PagoFacturaSerializer,
    ListFacturaSerializer,
    BoletaSerializer,
    BoletaSaveSerializer,
    CuadreVentaSerializer,
    MontosFaltantesSerializer,
    ResetMontosFaltantesSerializer,
    LiquidacionProveedorReporteSerialier,
    LiquidacionFacturaProveedorReporteSerialier
)
#app reportes
from applications.reportes.models import DetailVoucher, Voucher

#app caja
from applications.caja.models import Payment

#app recepcion
from applications.recepcion.models import DetailGuide
#
from .models import PaymentVoucher, Boleta, DetailBoleta
#
from .functions import emitir_boleta


class ListFacturaViewSet(viewsets.ModelViewSet):
    """ lista facturas a pagar"""

    serializer_class = ListFacturaSerializer

    def get_queryset(self):
        return Voucher.objects.filter(
            anulate=False,
            state=False
        )


class PagoFacturaViewSet(viewsets.ViewSet):
    """servcio que crear un pago de factura"""

    def create(self, request, *args, **kwargs):
        #guardamos los detalles
        for data in request.data:
            #serializamos la data
            serializado = PagoFacturaSerializer(data=data)
            if serializado.is_valid():
                #recuperamo el Voucher
                voucher = Voucher.objects.get(
                    number=serializado.validated_data['factura'],
                    anulate=False
                )
                if ((voucher.amount + 2) <  (serializado.validated_data['monto_real'])):
                    diferencia = True
                else:
                    diferencia = False

                #registramos el pago
                pago = PaymentVoucher(
                    factura=voucher,
                    codigo_pago=serializado.validated_data['codigo_pago'],
                    date_pago=serializado.validated_data['date_pago'],
                    responsabilidad=serializado.validated_data['responsabilidad'],
                    monto_real=serializado.validated_data['monto_real'],
                    monto_factura=voucher.amount,
                    diferencia=diferencia,
                    user_created=self.request.user,
                    user_modified=self.request.user
                )

                pago.save()
                #
                voucher.state = True
                voucher.save()
                print 'se  registro el pago'

                res = {'respuesta':'Guardado Correctamente','id':'0'}
            else:
                res = {'respuesta':'ya existe el numero de guia','id':'1'}
                print serializado.errors

        return Response(res)


class EmitirBoletaViewSet(viewsets.ModelViewSet):
    """ servicio para emitir boletas"""

    serializer_class = BoletaSerializer

    def get_queryset(self):
        date = self.kwargs['date']
        rs = self.kwargs['rs']
        dep = self.kwargs['dep']
        return emitir_boleta(date, rs, dep)


class AddBoletaViewSet(viewsets.ViewSet):
    """  servicio para guardar boleta """

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
                detail_guide = DetailGuide.objects.get(
                    pk=serializado.validated_data['detail_guide']
                )
                #guardamos la dealle boleta
                detail_boleta = DetailBoleta(
                    boleta=boleta,
                    detail_guide=detail_guide,
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


class CuadreVentaViewSet(viewsets.ModelViewSet):
    """ servicio para listar ventas en un periodo de tiempo"""

    serializer_class = CuadreVentaSerializer

    def get_queryset(self):
        date1 = self.kwargs['date1']
        date2 = self.kwargs['date2']
        return Payment.objects.cuadre_ventas_date(date1,date2)


class MontosFaltantesViewSet(viewsets.ModelViewSet):
    """ Vista para listar perdidas por area """

    serializer_class = MontosFaltantesSerializer

    def get_queryset(self):
        return PaymentVoucher.objects.filter(saldado=False, diferencia=False)


class ResetMontosFaltantesViewSet(viewsets.ViewSet):
    """servcio que crear reiniciar faltantes"""

    def create(self, request, *args, **kwargs):
        #guardamos los detalles
        for data in request.data:
            #serializamos la data
            serializado = ResetMontosFaltantesSerializer(data=data)
            if serializado.is_valid():
                #recuperamo el Voucher
                id_pv = serializado.validated_data['pk']
                #
                pv = PaymentVoucher.objects.get(pk=id_pv)
                #actualizamos el voucher
                pv.saldado = True
                print 'cuenta saldada'
                pv.save()
                res = {'respuesta':'Guardado Correctamente','id':'0'}
            else:
                res = {'respuesta':'No se pudo guardar','id':'1'}
                print serializado.errors

        return Response(res)


class LiquidacionProveedorReporteVieset(viewsets.ModelViewSet):
    """ Vista para reporte de compra total """

    serializer_class = LiquidacionProveedorReporteSerialier

    def get_queryset(self):
        #recuperamos datos de url
        q = self.kwargs['pro']
        r = self.kwargs['rs']
        s = self.kwargs['dep']
        #
        queryset = Payment.objects.movimientos_by_guia_by_departamento(q,r,s)
        return queryset


class LiquidacionFacturaProveedorReporteVieset(viewsets.ModelViewSet):
    """ Vista para reporte de compra facturada """

    serializer_class = LiquidacionFacturaProveedorReporteSerialier

    def get_queryset(self):
        #recuperamos datos de url
        q = self.kwargs['pro']
        r = self.kwargs['dep']
        s = self.kwargs['rs']
        t = self.kwargs['date']
        #
        queryset = Payment.objects.movimientos_by_guia_by_departamento_facturado(q,r,s,t)
        return queryset
