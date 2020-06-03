# -*- encoding: utf-8 -*-
from rest_framework import serializers
from .models import Provider, Vendor

class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = (
            'pk',
            'name',
        )

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = (
            'dni',
            'name',
        )


class VendorAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = (
            'cod',
            'pk',
            'dni',
            'name',
            'type_vendor',
            'seudonimo',
            'line_credit',
            'disable',
        )
