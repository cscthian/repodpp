# -*- encoding: utf-8 -*-
from rest_framework import viewsets, generics

from .models import Provider, Vendor, Departamento
from .serializers import (
    ProviderSerializer,
    VendorSerializer,
    VendorAllSerializer,
    DepartamentoSerializer
)


class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.filter(
        disable=False,
    )
    serializer_class = ProviderSerializer


class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer


class VendorListViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.filter(
        type_vendor='0',
        anulate=False,
    )
    serializer_class = VendorSerializer


class VendorAllListViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.filter(
        anulate=False,
    )
    serializer_class = VendorAllSerializer
