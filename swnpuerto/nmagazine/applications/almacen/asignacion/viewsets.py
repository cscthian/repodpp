# -*- encoding: utf-8 -*-
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from datetime import datetime

from .models import Asignation, DetailAsignation,Pauta, DetailPauta, Receptors
from .serializers import (
    DetailAsignationSerializer,
    DAsignationSerializer,
    DetAsignationSerializer,
    UpdateAsignationSerializer,
    PuataDinamicaSerializer,
    AsignationListSerializer,
    ConsultaSerializer,
    PautaProdSerializer,
    PautaProdAddSerializer,
    DetailAsignationListSerializer,
    EnabledPautaSerializer,
)
from .functions import (
    generar_pauta_dinamica,
    generar_consulta,
    generar_pauta_fija,
    cargar_asignacion,
    cargar_pauta,
)

from applications.almacen.recepcion.models import DetailGuide
from applications.almacen.entidad.models import Vendor
from applications.caja.pagos.models import Payment


class DetailAsignationViewSet(viewsets.ModelViewSet):
    """servicio para generar una pauta fija para Canillas"""
    serializer_class = DAsignationSerializer

    def get_queryset(self):
        pk_dg = self.kwargs['pk']
        dg = DetailGuide.objects.get(pk=pk_dg)
        return generar_pauta_fija(dg)


class UpdateAsignationViewSet(viewsets.ModelViewSet):
    """servicio para modificar ultima asignacion"""
    serializer_class = UpdateAsignationSerializer

    def get_queryset(self):
        pk_dg = self.kwargs['pk']
        dg = DetailGuide.objects.get(pk=pk_dg)
        return cargar_asignacion(dg)


class GenerarPautaDinamica(viewsets.ModelViewSet):
    """servicio para generar pauta multiple"""
    serializer_class =  PuataDinamicaSerializer

    def get_queryset(self):
        dia = self.kwargs['dia']
        return generar_pauta_dinamica(dia)


class AsignationListViewSet(viewsets.ModelViewSet):
    """servico que lista asignaciones"""
    serializer_class = AsignationListSerializer

    def get_queryset(self):
        date1 = self.kwargs['date1']
        date2 = self.kwargs['date2']
        queryset = Asignation.objects.filter(
            anulate=False,
            created__range=(date1,date2),
        ).order_by('-created')
        return queryset


class DetailAsignationListViewSet(viewsets.ModelViewSet):
    """servicio que lista detalle asignaciones"""
    serializer_class = DetailAsignationListSerializer

    def get_queryset(self):
        tipo = self.kwargs['tipo']
        return DetailAsignation.objects.filter(
            anulate=False,
            asignation__detail_guide__magazine_day__magazine__tipo=tipo,
        ).order_by('-created')[:100]


class DACreateViewSet(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        #recuperamos el DetalleMagaine
        pk_dm = self.kwargs['pk']
        dmagazine = DetailGuide.objects.get(pk=pk_dm)
        for data in request.data:
            #serializamos la data
            serializado = DetAsignationSerializer(data=data)
            if serializado.is_valid():
                #recuperamos canilla
                canilla_id = serializado.validated_data['pk']
                canilla = Vendor.objects.get(pk=canilla_id)
                #verificamos si existe o no una asigancion
                asig, created = Asignation.objects.get_or_create(
                    detail_guide=dmagazine,
                    anulate=False,
                    defaults={
                        'date':datetime.now(),
                        'user_created': self.request.user,
                    }
                )

                if created == False:
                    #verificamos si ya existe detale asigancion
                    da, cread = DetailAsignation.objects.update_or_create(
                        vendor=canilla,
                        asignation=asig,
                        defaults={
                            'count':serializado.validated_data['count'],
                            'precio_venta':dmagazine.precio_unitario,
                            'user_created':self.request.user,
                        }
                    )
                    #registramos la asignation detalle
                    da.user_modified = self.request.user
                    da.save()
                    print 'se a modificado la asignacion detalle'
                else:
                    #registramos la asignacion detalle
                    dasignation = DetailAsignation(
                        vendor=canilla,
                        asignation=asig,
                        count=serializado.validated_data['count'],
                        precio_venta=dmagazine.precio_unitario,
                        user_created=self.request.user,
                    )
                    dasignation.save()
                    print 'se a creado la asinacion detalle'
                    dmagazine.asignado = True
                    dmagazine.save()
            else:
                print serializado.errors
        return Response()


#funcion para crear un pauta
class RegisterPautaView(viewsets.ViewSet):
    """funcion que crea registra pautas"""

    def create(self, request, *args, **kwargs):
        #recuperamos el DetalleMagaine
        pk_dm = self.kwargs['pk']
        dmagazine = DetailGuide.objects.get(pk=pk_dm)
        #actualizamos el numero de guia
        ser = DAsignationSerializer(data=request.data[0])
        if ser.is_valid():
            dmagazine.guide.number = ser.validated_data['guia']
            dmagazine.guide.user_modified = self.request.user
            dmagazine.guide.save()
            print "----se actualizo la guia---"
        #regitrsmos el detalle pauta
        for data in request.data:
            #serializamos la data
            serializado = DAsignationSerializer(data=data)
            if serializado.is_valid():
                #recuperamos canilla
                canilla_id = serializado.validated_data['pk']
                canilla = Vendor.objects.get(pk=canilla_id)
                #verificamos si existe o no una asigancion
                pauta, created = Pauta.objects.get_or_create(
                    detail_guide=dmagazine,
                    anulate=False,
                    defaults={
                        'date':datetime.now(),
                        'user_created': self.request.user,
                    }
                )

                if created == False:
                    #verificamos si ya existe detale asigancion
                    da, cread = DetailPauta.objects.update_or_create(
                        vendor=canilla,
                        pauta=pauta,
                        defaults={
                            'count':serializado.validated_data['count'],
                            'user_created':self.request.user,
                        }
                    )
                    #registramos la asignation detalle
                    da.user_modified = self.request.user
                    da.save()
                    print 'se a modificado la pauta detalle'
                else:
                    #registramos la asignacion detalle
                    dasignation = DetailPauta(
                        vendor=canilla,
                        pauta=pauta,
                        count=serializado.validated_data['count'],
                        user_created=self.request.user,
                    )
                    dasignation.save()
                    print 'se a creado la pauta detalle'
                    dmagazine.asignado = True
                    dmagazine.save()
            else:
                print serializado.errors
        return Response()


class EnabledPautaView(viewsets.ViewSet):
    """Vista para habilitar o inabilitar pauata"""

    def create(self, request, *args, **kwargs):
        #recuperamos el DetalleMagaine
        pk_dm = self.kwargs['pk']
        dmagazine = DetailGuide.objects.get(pk=pk_dm)
        #actualizamos el numero de guia
        serializado = EnabledPautaSerializer(data=request.data)
        if serializado.is_valid():
            #recuperamos la puata y actualzamos estado enabled
            pauta = Pauta.objects.get(
                detail_guide=dmagazine,
                anulate=False,
            )
            pauta.enabled = serializado.validated_data['enabled']
            pauta.save()
            print '=====Pauta Habilitada===='
            #
            dmagazine.guide.number = serializado.validated_data['guia']
            dmagazine.guide.save()
            #
            dmagazine.en_reparto = serializado.validated_data['enabled']
            dmagazine.save()
        else:
            print serializado.errors

        return Response()


class UpdatePautaView(viewsets.ModelViewSet):
    """servicio para modificar ultima Pauta"""
    serializer_class = UpdateAsignationSerializer

    def get_queryset(self):
        pk_dg = self.kwargs['pk']
        print '===codigo===='
        print pk_dg
        dg = DetailGuide.objects.get(pk=pk_dg)
        return cargar_pauta(dg)


class CargarPautaView(viewsets.ModelViewSet):
    """servicio para CARGAR Pauta"""
    serializer_class = PautaProdSerializer

    def get_queryset(self):
        cod = self.kwargs['cod']
        tipo = self.kwargs['pk']
        return DetailPauta.objects.filter(
            pauta__enabled=True,
            pauta__detail_guide__magazine_day__magazine__tipo=tipo,
            vendor__cod=cod,
            asignado=False,
            count__gte=1,
        )


class RegisterEntregaProdView(viewsets.ViewSet):
    """Vista para Registrar Entrega de Productos"""

    def create(self, request, *args, **kwargs):
        canilla = Vendor.objects.get(cod=self.kwargs['cod'])
        dni = self.kwargs['dni']

        for data in request.data:
            #serializamos la data
            serializado = PautaProdAddSerializer(data=data)
            if serializado.is_valid():
                #recuperamos el detail guide
                if (int(serializado.validated_data['count']) > 0):
                    detail_guide = DetailGuide.objects.get(pk=serializado.validated_data['detail_guide'])

                    #creamos o recuperamos la asignacion
                    asignation, created = Asignation.objects.get_or_create(
                        detail_guide=detail_guide,
                        anulate=False,
                        defaults={
                            'date':datetime.now(),
                            'user_created': self.request.user,
                        }
                    )

                    detail_asignation, cread = DetailAsignation.objects.update_or_create(
                        vendor=canilla,
                        asignation=asignation,
                        defaults={
                            'count':serializado.validated_data['count'],
                            'precio_venta':detail_guide.precio_unitario,
                            'user_created':self.request.user,
                        }
                    )
                    detail_asignation.user_modified = self.request.user
                    detail_asignation.save()

                    #guardamos el receptor
                    receptor, created = Receptors.objects.update_or_create(
                        detail_asignation=detail_asignation,
                        defaults={
                            'dni':dni,
                            'user_created':self.request.user,
                        }
                    )
                    receptor.user_modified = self.request.user
                    receptor.save()
                    print '===el registro de guardo correctamente==='
                    #actualizmos como asignado
                    pauta_detalle = DetailPauta.objects.filter(
                        asignado=False,
                        vendor=canilla,
                        pauta__detail_guide=detail_guide,
                    )[0]
                    pauta_detalle.asignado = True
                    pauta_detalle.save()
                    print '===actualizado como asignado==='

                else:
                    if serializado.validated_data['count'] == '-1':
                        detail_guide = DetailGuide.objects.get(pk=serializado.validated_data['detail_guide'])
                        pauta_detalle = DetailPauta.objects.filter(
                            asignado=False,
                            vendor=canilla,
                            pauta__detail_guide=detail_guide,
                        )[0]
                        pauta_detalle.asignado = True
                        pauta_detalle.count = 0
                        pauta_detalle.save()
                        print '===Se cancelo la Asignacion==='
            else:
                print serializado.errors

        return Response(serializado.errors)


class ConsultaViewSet(viewsets.ModelViewSet):
    serializer_class = ConsultaSerializer

    def get_queryset(self):
        pk_gd = self.kwargs['pk']
        return generar_consulta(pk_gd)
