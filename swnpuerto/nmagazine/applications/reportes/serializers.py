# -*- encoding: utf-8 -*-
from rest_framework import serializers

from applications.administrador.serializers import VentasSerializer
from applications.almacen.recepcion.serializers import CountListField, ProdListField

from .models import CierreMes

class CierreMesSerializer(serializers.ModelSerializer):
    user_created = serializers.CharField(source='user_created.username')
    mes = serializers.SerializerMethodField()
    class Meta:
        model = CierreMes
        fields = (
            'pk',
            'mes',
            'date_start',
            'date_end',
            'venta_neta',
            'ingreso_neto',
            'venta_neta_real',
            'ingreso_neto_real',
            'user_created',
        )

    def get_mes(self,obj):
        return obj.get_mes_display()


#ranking de diarios y productos
class MagazinRanking(serializers.Serializer):
    pk = serializers.CharField()
    name = serializers.CharField()
    vendido = serializers.IntegerField(required=False)
    devuelto = serializers.IntegerField(required=False)
    perdido = serializers.IntegerField(required=False)
    monto = serializers.DecimalField(max_digits=10, decimal_places=3)


#ranking de diarios y productos
class VendorRanking(serializers.Serializer):
    pk = serializers.CharField()
    cod = serializers.CharField()
    name = serializers.CharField()
    tipo = serializers.CharField()
    tope = serializers.DecimalField(max_digits=10, decimal_places=3)
    deuda = serializers.DecimalField(max_digits=10, decimal_places=3)
    entregado = serializers.IntegerField(required=False)
    vendido = serializers.IntegerField(required=False)
    devuelto = serializers.IntegerField(required=False)


#historial de canillas
class HistoriaSerializer(serializers.Serializer):
    pk = serializers.CharField()
    cod = serializers.CharField()
    name = serializers.CharField(required=False)
    tipo = serializers.CharField(required=False)
    puntaje = ProdListField()
    meses = ProdListField()

#canillas cero
class CeroSerializer(serializers.Serializer):
    pk = serializers.CharField()
    cod = serializers.CharField()
    name = serializers.CharField(required=False)
    tipo = serializers.CharField(required=False)
    lunes = serializers.IntegerField(required=False)
    martes = serializers.IntegerField(required=False)
    miercoles = serializers.IntegerField(required=False)
    jueves = serializers.IntegerField(required=False)
    viernes = serializers.IntegerField(required=False)
    sabado = serializers.IntegerField(required=False)
    domingo = serializers.IntegerField(required=False)


class HistoryGuideResumenSeriaizer(serializers.Serializer):
    total_vendido = serializers.DecimalField(max_digits=10, decimal_places=3)
    total_deuda = serializers.DecimalField(max_digits=10, decimal_places=3)
    total_almacen = serializers.DecimalField(max_digits=10, decimal_places=3)
    count_vendido = serializers.IntegerField(required=False)
    count_deuda = serializers.IntegerField(required=False)
    count_almacen = serializers.IntegerField(required=False)
    count_real = serializers.IntegerField(required=False)


#serializador para historial de guia
class HistoryGSerializer(serializers.Serializer):
    date = serializers.CharField()
    count_dev = serializers.IntegerField(required=False)
    count_ven = serializers.IntegerField(required=False)
    count_tie = serializers.IntegerField(required=False)


class HistoryGuideSerializer(serializers.Serializer):
    pk = serializers.CharField()
    magazine = serializers.CharField()
    count_reception = serializers.IntegerField(required=False)
    count_deliver = serializers.IntegerField(required=False)
    precio_venta = serializers.DecimalField(max_digits=10, decimal_places=3)
    historia = HistoryGSerializer(many=True)
    #
    total_vendido = serializers.DecimalField(max_digits=10, decimal_places=3)
    total_deuda = serializers.DecimalField(max_digits=10, decimal_places=3)
    total_almacen = serializers.DecimalField(max_digits=10, decimal_places=3)
    count_vendido = serializers.IntegerField(required=False)
    count_deuda = serializers.IntegerField(required=False)
    count_almacen = serializers.IntegerField(required=False)
    count_devuelto = serializers.IntegerField(required=False)
    count_real = serializers.IntegerField(required=False)


class ResumenDetalleGuiaSerializer(serializers.Serializer):
    magazine = serializers.CharField()
    count_reception = serializers.IntegerField(required=False)
    count_deliver = serializers.IntegerField(required=False)
    count_diferencia = serializers.IntegerField(required=False)
    precio_venta = serializers.DecimalField(max_digits=10, decimal_places=3)
    total_vendido = serializers.DecimalField(max_digits=10, decimal_places=3)
    total_deuda = serializers.DecimalField(max_digits=10, decimal_places=3)
    total_almacen = serializers.DecimalField(max_digits=10, decimal_places=3)
    count_vendido = serializers.IntegerField(required=False)
    count_devuelto = serializers.IntegerField(required=False)
    count_deuda = serializers.IntegerField(required=False)
    count_almacen = serializers.IntegerField(required=False)
    count_real = serializers.IntegerField(required=False)
    count_perdida = serializers.IntegerField(required=False)
    amount_perdida = serializers.DecimalField(max_digits=10, decimal_places=3)



class ResumenGuideSerializer(serializers.Serializer):
    number = serializers.CharField()
    provider = serializers.CharField()
    date = serializers.CharField()
    amount_perdida = serializers.DecimalField(max_digits=10, decimal_places=3)
    culmined = serializers.BooleanField(default=True)
    #
    itmes = ResumenDetalleGuiaSerializer(many=True)


class CountRealSerializer(serializers.Serializer):
    pk = serializers.CharField()
    count = serializers.IntegerField(required=False)
