# -*- encoding: utf-8 -*-

from rest_framework import serializers

class InventarioSerializer(serializers.Serializer):
    pk_diario = serializers.CharField()
    name = serializers.CharField(required=False)
    date = serializers.DateField()
    tipo = serializers.CharField(required=False)
    cantidad = serializers.IntegerField()


class CosntatarSerializer(serializers.Serializer):
    guia = serializers.CharField()
    pk_diario = serializers.CharField()
    name = serializers.CharField(required=False)
    count = serializers.IntegerField()
    real_count = serializers.IntegerField()
    missing = serializers.IntegerField()


class DetalleSerializer(serializers.Serializer):
    guia = serializers.CharField()
    fecha = serializers.DateTimeField()
    registrado = serializers.IntegerField()
    entregado = serializers.IntegerField()
    devuelto = serializers.IntegerField()
    lost_almacen = serializers.IntegerField()
    lost_caja = serializers.IntegerField()
    lost_trasporte = serializers.IntegerField()
    total = serializers.IntegerField()
