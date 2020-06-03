# -*- encoding: utf-8 -*-

from rest_framework import serializers
from .models import Magazine, Guide, MagazineDay, DetailGuide


class CountListField(serializers.ListField):
    child = serializers.IntegerField(
        min_value=1,
        max_value=100000,
    )


class ProdListField(serializers.ListField):
    child = serializers.CharField()


class MagazineSerializer(serializers.ModelSerializer):
    provider = serializers.CharField(source='provider.name')
    tipo = serializers.SerializerMethodField()
    class Meta:
        model = Magazine
        fields = (
            'pk',
            'name',
            'tipo',
            'provider',
            'description',
        )

    def get_tipo(self,obj):
        return obj.get_tipo_display()


class MagazineDaySerializer(serializers.ModelSerializer):
    magazine = serializers.CharField(source='magazine.name')
    day = serializers.SerializerMethodField()
    class Meta:
        model = MagazineDay
        fields = (
            'pk',
            'magazine',
            'day',
        )

    def get_day(self,obj):
        return obj.get_day_display()


class ProdSerializer(serializers.ModelSerializer):
    magazine = serializers.CharField(source='magazine.name')
    day = serializers.SerializerMethodField()
    class Meta:
        model = MagazineDay
        fields = (
            'pk',
            'magazine',
            'day',
            'precio_guia',
            'precio_venta',
            'precio_tapa',
        )

    def get_day(self,obj):
        return obj.get_day_display()


class GuideSerializer(serializers.Serializer):
    number = serializers.CharField()
    addressee = serializers.CharField()
    invoce = serializers.CharField(required=False)
    provider = serializers.CharField()
    plazo = serializers.IntegerField(required=False)
    counts = CountListField()
    prods = ProdListField()
    asignar = serializers.BooleanField(required=False)
    agente = serializers.CharField()


class GuideListSerializer(serializers.ModelSerializer):
    provider = serializers.CharField(source='provider.name')
    user_created = serializers.CharField(source='user_created.username')
    class Meta:
        model = Guide
        fields = (
            'pk',
            'number',
            'date',
            'number_invoce',
            'provider',
            'date_emission',
            'date_retunr_cargo',
            'created',
            'culmined',
            'asignado',
            'returned',
            'anulate',
            'user_created',
        )


class DetailGuideSerializer(serializers.ModelSerializer):
    magazine_day = serializers.CharField(source='magazine_day.pk')
    class Meta:
        model = DetailGuide
        fields = (
            'pk',
            'magazine_day',
            'count',
            'guide',
        )


class DetailGuideGetSerializer(serializers.ModelSerializer):
    magazine_day = serializers.CharField(source='magazine_day.magazine.name')
    class Meta:
        model = DetailGuide
        fields = (
            'pk',
            'magazine_day',
            'count',
            'precio_unitario',
        )


class DetailGuideListSerializer(serializers.ModelSerializer):
    magazine_day = serializers.SerializerMethodField()
    class Meta:
        model = DetailGuide
        fields = (
            'pk',
            'magazine_day',
            'count',
            'guide',
            'discount',
            'created',
            'asignado',
            'en_reparto',
        )

    def get_magazine_day(self,obj):
        return obj.magazine_day.magazine.name +' '+ obj.magazine_day.get_day_display()


class PorCobrarListSerializer(serializers.ModelSerializer):
    magazine_day = serializers.SerializerMethodField()
    guide = serializers.CharField(source='guide.number')
    class Meta:
        model = DetailGuide
        fields = (
            'pk',
            'magazine_day',
            'count',
            'guide',
            'discount',
            'created',
            'asignado',
        )

    def get_magazine_day(self,obj):
        return obj.magazine_day.magazine.name +' '+ obj.magazine_day.get_day_display()


class DGcreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailGuide
        fields = (
            'pk',
            'magazine_day',
            'count',
            'guide',
        )
