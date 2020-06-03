# -*- encoding: utf-8 -*-
from rest_framework import serializers

from .models import DetailAsignation, Asignation, DetailPauta

from applications.almacen.recepcion.serializers import CountListField, ProdListField

class DetailAsignationSerializer(serializers.ModelSerializer):
    asignation = serializers.CharField(source='asignation.vendor.name')
    class Meta:
        model = DetailAsignation
        fields = (
            'asignation',
            'count',
        )


class DetAsignationSerializer(serializers.Serializer):
    pk = serializers.CharField()
    cod = serializers.CharField()
    name = serializers.CharField(required=False)
    tipo = serializers.CharField(required=False)
    count = serializers.IntegerField(required=False)
    diario = serializers.CharField()
    date = serializers.DateField()


class DAsignationSerializer(serializers.Serializer):
    pk = serializers.CharField()
    cod = serializers.CharField()
    guia = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    tipo = serializers.CharField(required=False)
    count = serializers.IntegerField(required=False)
    diario = serializers.CharField()
    date = serializers.DateField()


class UpdateAsignationSerializer(DAsignationSerializer):
    mje = serializers.CharField()


class ConsultaSerializer(serializers.Serializer):
    pk = serializers.CharField()
    cod = serializers.CharField()
    name = serializers.CharField(required=False)
    count = serializers.IntegerField(required=False)
    returned = serializers.IntegerField(required=False)
    total = serializers.IntegerField(required=False)
    total_returned = serializers.IntegerField(required=False)
    diario = serializers.CharField()
    date = serializers.DateField()
    receptor = serializers.CharField()


class PuataDinamicaSerializer(serializers.Serializer):
    pk = serializers.CharField()
    cod = serializers.CharField()
    name = serializers.CharField(required=False)
    count = CountListField()
    product = ProdListField()


class AsignationListSerializer(serializers.ModelSerializer):
    detail_guide = serializers.CharField(source='detail_guide.magazine_day.magazine')
    class Meta:
        model = Asignation
        fields = (
            'pk',
            'detail_guide',
            'date',
            'user_created',
        )


class PautaProdSerializer(serializers.ModelSerializer):
    vendor = serializers.CharField(source='vendor.name')
    precio_venta = serializers.SerializerMethodField()
    magazine = serializers.SerializerMethodField()
    detail_guide = serializers.CharField(source='pauta.detail_guide.pk')
    class Meta:
        model = DetailPauta
        fields = (
            'pk',
            'count',
            'vendor',
            'magazine',
            'precio_venta',
            'detail_guide',
        )
    def get_precio_venta(self,obj):
        return obj.pauta.detail_guide.precio_unitario

    def get_magazine(self,obj):
        dias = [
            '[Lunes]',
            '[Martes]',
            '[Miercoles]',
            '[Jueves]',
            '[Viernes]',
            '[Sabado]',
            '[Domingo]',
            '[Lunes-sabado]',
        ]
        if obj.pauta.detail_guide.magazine_day.magazine.tipo == '0':
            return obj.pauta.detail_guide.magazine_day.magazine.name + dias[int(obj.pauta.detail_guide.magazine_day.day)]
        else:
            return obj.pauta.detail_guide.magazine_day.magazine.name


class PautaProdAddSerializer(serializers.Serializer):
    detail_guide = serializers.CharField()
    count = serializers.CharField()


class DetailAsignationListSerializer(serializers.ModelSerializer):
    asignation = serializers.CharField(source='asignation.detail_guide.magazine_day')
    class Meta:
        model = DetailAsignation
        fields = (
            'pk',
            'asignation',
            'count',
        )


class EnabledPautaSerializer(serializers.Serializer):
    """serializador para habilitar inabilitar pauta"""
    guia = serializers.CharField()
    enabled = serializers.BooleanField()
