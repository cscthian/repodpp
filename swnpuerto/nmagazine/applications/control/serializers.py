# -*- encoding: utf-8 -*-
from rest_framework import serializers


class VoucherSerializer(serializers.Serializer):
    guide = serializers.CharField()
    voucher = serializers.CharField()
    date = serializers.DateField(required=False)
