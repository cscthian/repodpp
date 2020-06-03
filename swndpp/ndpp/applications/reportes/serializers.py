# -*- encoding: utf-8 -*-

from rest_framework import serializers
from .models import DetailVoucher

#app recepcion
from applications.recepcion.models import DetailGuide

class VoucherGuideSerializer(serializers.ModelSerializer):
    """serializador para agregar guias a una factura"""

    class Meta:
        model = DetailVoucher
        fields = (
            'voucher',
            'dettail_guide',
        )


class DeleteVoucherGuideSerializer(serializers.Serializer):
    """serializador para agregar guias a una factura"""

    voucher = serializers.CharField()


class GuideItemsSerializer(serializers.Serializer):
    """serializador para listar items de una guia por voucher"""

    magazine_day = serializers.SerializerMethodField()
    guide = serializers.CharField(source='dettail_guide.guide.number')
    pk = serializers.CharField(source='id')
    count = serializers.IntegerField(source='dettail_guide.count')
    precio_unitario = serializers.DecimalField(max_digits=10, decimal_places=3, source='dettail_guide.precio_unitario')
    precio_guia = serializers.DecimalField(max_digits=10, decimal_places=3, source='dettail_guide.precio_guia')
    date = serializers.DateField(source='dettail_guide.guide.date_emission')

    class Meta:
        model = DetailVoucher
        fields = (
            'pk',
            'magazine_day',
            'guide',
            'count',
            'precio_unitario',
            'precio_guia',
            'date',
        )
    #
    def get_magazine_day(self,obj):
        return str(obj.dettail_guide.magazine_day.magazine.name) + '-' + str(obj.dettail_guide.magazine_day.get_day_display())


class SearchDetailGuideSerializer(serializers.ModelSerializer):
    """serializador para agregar guias a una factura"""

    provider = serializers.CharField(source='guide.provider.name')
    departamento = serializers.CharField(source='guide.departamento.name')
    guide = serializers.CharField(source='guide.number')
    magazine_day = serializers.SerializerMethodField()
    date = serializers.DateField(source='guide.date_emission')
    state = serializers.BooleanField(required=False, default=True)

    class Meta:
        model = DetailGuide
        fields = (
            'id',
            'facturado',
            'magazine_day',
            'guide',
            'count',
            'precio_unitario',
            'precio_guia',
            'departamento',
            'provider',
            'date',
            'state',
        )
    #
    def get_magazine_day(self,obj):
        return str(obj.magazine_day.magazine.name) + '-' + str(obj.magazine_day.get_day_display())
