# -*- encoding: utf-8 -*-
from rest_framework import serializers

from applications.almacen.recepcion.models import DetailGuide, Guide

class LiquidacionDiaSerializer(serializers.Serializer):
    pk_diario = serializers.CharField()
    diario = serializers.CharField()
    time = serializers.DateTimeField()
    devuelto = serializers.IntegerField(required=False)
    pagado = serializers.IntegerField(required=False)
    monto = serializers.DecimalField(max_digits=10, decimal_places=3)


class VendorSerializer(serializers.Serializer):
    pk = serializers.CharField()
    canilla = serializers.CharField()
    seudonimo = serializers.CharField()
    tipo = serializers.CharField()
    movimientos = LiquidacionDiaSerializer(many=True)


class MovimientosSerializer(serializers.Serializer):
    magazine = serializers.CharField()
    dia = serializers.CharField()
    created = serializers.DateTimeField()
    entregado = serializers.CharField()
    count_return = serializers.IntegerField()
    count_payment= serializers.IntegerField()
    debe = serializers.IntegerField()
    precio = serializers.DecimalField(max_digits=10, decimal_places=3)
    #monto_deuda = serializers.DecimalField(max_digits=10, decimal_places=3)
    amount = serializers.DecimalField(max_digits=10, decimal_places=3)


class MovimientosCanillaSerializer(serializers.Serializer):
    cod = serializers.CharField()
    name = serializers.CharField()
    seudonimo = serializers.CharField()
    total = serializers.DecimalField(max_digits=10, decimal_places=3)
    movimientos = MovimientosSerializer(many=True)


class LiquidacionRangoSerializer(serializers.ModelSerializer):
    magazine_day = serializers.CharField()
    precio_guia = serializers.DecimalField(max_digits=10, decimal_places=3)
    precio_venta = serializers.DecimalField(max_digits=10, decimal_places=3)
    devuelto = serializers.IntegerField(required=False)
    vendido = serializers.IntegerField(required=False)

    class Meta:
        model = DetailGuide
        fields = (
            'magazine_day',
            'count',
            'precio_guia',
            'precio_venta',
            'devuelto',
            'vendido',
        )

class GudeSerializer(serializers.ModelSerializer):
    provider = serializers.CharField(source='provider.name')
    detalle = LiquidacionRangoSerializer(many=True)
    class Meta:
        model = Guide
        fields = (
            'number',
            'date',
            'number_invoce',
            'provider',
            'detalle',
        )


class GuiaSerializer(serializers.Serializer):
    factura = serializers.CharField()
    guide = serializers.CharField()
    magazine = serializers.CharField()
    date = serializers.DateField()
    count = serializers.IntegerField(required=False)
    amount_total = serializers.DecimalField(max_digits=10, decimal_places=3)
    precio_unitario = serializers.DecimalField(max_digits=10, decimal_places=3)
    devuelto = serializers.IntegerField(required=False)
    vendido = serializers.IntegerField(required=False)
    amount_vendido = serializers.DecimalField(max_digits=10, decimal_places=3)
    provider = serializers.CharField()
    amount = serializers.CharField()
    total = serializers.DecimalField(max_digits=10, decimal_places=3)


class ResumenPagosSerializer(serializers.Serializer):
    guide = serializers.CharField()
    date = serializers.CharField()
    dia = serializers.CharField()
    magazine = serializers.CharField()
    precio = serializers.DecimalField(max_digits=10, decimal_places=3)
    devuelto = serializers.IntegerField(required=False)
    pagado = serializers.IntegerField(required=False)
    total = serializers.DecimalField(max_digits=10, decimal_places=3)


class LiquidacionProveedorSerializer(serializers.Serializer):
    name = serializers.CharField()
    sub_total = serializers.DecimalField(max_digits=10, decimal_places=3)
    lista_pagos = ResumenPagosSerializer(many=True)
