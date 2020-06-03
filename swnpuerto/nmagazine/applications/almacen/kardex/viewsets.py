from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from django.utils import timezone

from datetime import datetime, timedelta

from applications.almacen.recepcion.models import (
    Magazine,
    Guide,
    MagazineDay,
    DetailGuide,
)

from .serializers import (
    InventarioSerializer,
    CosntatarSerializer,
    DetalleSerializer,
)

from .functions import magazine_inventario, magazine_constatar, magazine_detalle


class InventarioListViewSet(viewsets.ModelViewSet):
    """vista que lista inventario de magazines"""
    serializer_class = InventarioSerializer

    def get_queryset(self):
        end_date = timezone.now() + timedelta(days=1)
        start_date = end_date - timedelta(days=30)
        detail_guides = DetailGuide.objects.filter(
            anulate=False,
            created__range=(start_date, end_date),
        ).order_by('-created')
        return magazine_inventario(detail_guides)


class ConstatarListViewSet(viewsets.ModelViewSet):
    """vista para listar diario/producto no culminado"""
    serializer_class = CosntatarSerializer

    def get_queryset(self):
        guide = self.kwargs['guide']
        return magazine_constatar(guide)


class DetalleViewSet(viewsets.ModelViewSet):
    """vista para mostrar los movimientos de un magazine"""
    serializer_class = DetalleSerializer

    def get_queryset(self):
        guide = self.kwargs['guide']
        return magazine_detalle(guide)


class ConstatarCreateView(viewsets.ViewSet):
    """clase para registrar diarios o productos perdidos"""

    def create(self, request, *args, **kwargs):
        #recuperamos data enviada por POST
        for data in request.data:
            #serializamos la data
            serializado = CosntatarSerializer(data=data)
            #verificamos que la data sea valida
            if serializado.is_valid():
                #recuperamos data
                guia = serializado.validated_data['guia']
                diario = serializado.validated_data['pk_diario']
                missing = serializado.validated_data['missing']

                #actualizmos perdida
                if missing > 0:
                    detail_guide = DetailGuide.objects.get(
                        anulate=False,
                        culmined=False,
                        guide__number=guia,
                        magazine_day__pk=diario,
                    )
                    detail_guide.missing = missing
                    detail_guide.save()

        return Response()
