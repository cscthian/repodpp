# -*- encoding: utf-8 -*-
from rest_framework import serializers
from applications.recepcion.models import DetailGuide


class PagoSerializer(serializers.Serializer):
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
    date = serializers.DateField(required=False)
    number_operation = serializers.CharField()
    date_operation = serializers.DateField()
    vencido = serializers.CharField(required=False)
