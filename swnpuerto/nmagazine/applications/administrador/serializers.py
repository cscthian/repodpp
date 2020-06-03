# -*- encoding: utf-8 -*-
from rest_framework import serializers

from .models import LostMagazine, Boleta

class VentasSerializer(serializers.Serializer):
    label = serializers.CharField()
    value = serializers.DecimalField(max_digits=10, decimal_places=3)


class NotaItesSerializer(serializers.Serializer):
    pk = serializers.CharField()
    name = serializers.CharField()
    precio_guia = serializers.DecimalField(max_digits=10, decimal_places=3)
    precio_venta = serializers.DecimalField(max_digits=10, decimal_places=3)
    count = serializers.IntegerField()
    date = serializers.DateField()


class BoletaSerializer(serializers.Serializer):
    pk = serializers.CharField()
    total = serializers.DecimalField(max_digits=10, decimal_places=3)
    codigo = serializers.CharField()
    magazine = serializers.CharField()
    number = serializers.CharField()
    client = serializers.CharField()
    date_emition = serializers.DateField()
    date_venta = serializers.DateField()
    count = serializers.IntegerField()
    precio_venta = serializers.DecimalField(max_digits=10, decimal_places=3)
    precio_sunat = serializers.DecimalField(max_digits=10, decimal_places=3)
    amount = serializers.DecimalField(max_digits=10, decimal_places=3)
    afecto = serializers.BooleanField()
    addressee = serializers.CharField()
    vendor = serializers.CharField(required=False)
    emitido = serializers.BooleanField()
    impreso = serializers.BooleanField()


class BoletaSaveSerializer(serializers.Serializer):
    pk = serializers.CharField()
    total = serializers.DecimalField(max_digits=10, decimal_places=3)
    magazine = serializers.CharField()
    number = serializers.CharField()
    client = serializers.CharField()
    date_emition = serializers.DateField()
    date_venta = serializers.DateField()
    count = serializers.IntegerField()
    precio_venta = serializers.DecimalField(max_digits=10, decimal_places=3)
    precio_sunat = serializers.DecimalField(max_digits=10, decimal_places=3)
    amount = serializers.DecimalField(max_digits=10, decimal_places=3)
    afecto = serializers.BooleanField()
    addressee = serializers.CharField()
    impreso = serializers.BooleanField()

class BoletaListSerializer(serializers.ModelSerializer):
    user_created = serializers.CharField(source='user_created.username')
    razon_social = serializers.SerializerMethodField()
    class Meta:
        model = Boleta
        fields = (
            'pk',
            'number',
            'client',
            'date_emition',
            'date_venta',
            'razon_social',
            'amount',
            'igv',
            'afecto',
            'anulate',
            'user_created',
            'created',
        )

    def get_razon_social(self,obj):
        return obj.get_razon_social_display()


class LostSerializer(serializers.ModelSerializer):
    class Meta:
        model = LostMagazine
        fields = (
            'module',
            'detail_guide',
            'count',
            'description',
        )


class LostListSerializer(serializers.ModelSerializer):
    module = serializers.SerializerMethodField()
    detail_guide = serializers.SerializerMethodField()
    class Meta:
        model = LostMagazine
        fields = (
            'pk',
            'module',
            'detail_guide',
            'count',
            'precio_venta',
            'description',
        )

    def get_module(self,obj):
        return obj.get_module_display()

    def get_detail_guide(self,obj):
        return str(obj.detail_guide.magazine_day)


class ReiniciarCuentaSerializer(serializers.Serializer):
    module = serializers.CharField()
