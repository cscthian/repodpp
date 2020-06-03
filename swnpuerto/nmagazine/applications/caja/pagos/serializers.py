# -*- encoding: utf-8 -*-
from rest_framework import serializers
from applications.almacen.recepcion.models import DetailGuide
from applications.almacen.recepcion.serializers import ProdListField


class PagoSerializer(serializers.Serializer):
    estado = serializers.CharField()
    guide = serializers.CharField()
    pk_asignation = serializers.CharField()
    diario = serializers.CharField()
    tipo = serializers.CharField()
    canilla = serializers.CharField()
    entregado = serializers.IntegerField(required=False)
    devuelto = serializers.IntegerField(required=False)
    pagar = serializers.IntegerField(required=False)
    deuda = serializers.IntegerField(required=False)
    precio_venta = serializers.DecimalField(max_digits=10, decimal_places=3)
    amount = serializers.DecimalField(max_digits=10, decimal_places=3,required=False)
    boleta = serializers.IntegerField(required=False)
    vencido = serializers.BooleanField()
    por_vencer = ProdListField()
    date = serializers.DateField(required=False)


class CuadrarCajaSerializer(serializers.Serializer):
    date = serializers.DateField()
    magazine = serializers.CharField()
    tipo = serializers.CharField()
    devuelto = serializers.IntegerField()
    cantidad = serializers.IntegerField()
    precio_venta = serializers.DecimalField(max_digits=10, decimal_places=3)
    monto = serializers.DecimalField(max_digits=10, decimal_places=3)


class ProdVentaSerializer(serializers.Serializer):
    pk = serializers.CharField()
    magazine = serializers.CharField()


class RegisterVentaSerializer(serializers.Serializer):
    pk = serializers.CharField()
    count = serializers.IntegerField()


class GetProdSerializer(serializers.Serializer):
    class Meta:
        model = DetailGuide
        fields = (
            'pk',
            'magazine_day',
            'precio_unitario',
        )
