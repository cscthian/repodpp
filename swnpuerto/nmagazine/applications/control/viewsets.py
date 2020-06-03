# -*- encoding: utf-8 -*-

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from datetime import datetime

from .serializers import VoucherSerializer

from .models import Voucher, DetailVoucher

from applications.almacen.recepcion.models import Guide


class AddVoucherViewSet(viewsets.ViewSet):
    """servcio que crear un nuevo registro Voucher"""

    def create(self, request, *args, **kwargs):

        #iteramos el json y guardamos los detalles
        res = {'respuesta':'Guardado Correctamente','id':'0'}
        for data in request.data:
            #serializamos la data
            serializado = VoucherSerializer(data=data)
            if serializado.is_valid():
                #recuperamo la guia
                guia = Guide.objects.get(number=serializado.validated_data['guide'])
                #creamos el voucher
                obj, created = Voucher.objects.get_or_create(
                    number=serializado.validated_data['voucher'],
                    defaults = {
                        'user_created':self.request.user,
                        'date':serializado.validated_data['date'],
                    },
                )
                if created == False:
                    valido = Voucher.objects.es_valido(
                        serializado.validated_data['voucher'],
                        serializado.validated_data['date']
                    )
                    if valido:
                        voucher_detail = DetailVoucher(
                            voucher=obj,
                            guide=guia,
                            user_created=self.request.user,
                        )
                        #guardamos el registro
                        voucher_detail.save()
                        print 'voucher creado'

                    else:
                        print '======no es valido====='
                        res = {'respuesta':'Voucher '+serializado.validated_data['voucher']+' ya esta Registrado Anteriormente','id':'1'}
                else:
                    voucher_detail = DetailVoucher(
                        voucher=obj,
                        guide=guia,
                        user_created=self.request.user,
                    )
                    #guardamos el registro
                    voucher_detail.save()
                    print 'voucher nuevo creado'
            else:
                res = {'respuesta':'Los Datos no son Validos','id':'1'}
                print serializado.errors

        return Response(res)


class RecuperarVoucherViewSet(viewsets.ModelViewSet):
    """servicio que carga detalle vouchers creados"""
    serializer_class = VoucherSerializer

    def get_queryset(self):
        date = self.kwargs['date']
        return DetailVoucher.objects.vouchers_by_date(date)
