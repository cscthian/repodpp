# -*- encoding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework import routers
from . import views

from .viewsets import (
    ProviderViewSet,
    VendorListViewSet,
    VendorAllListViewSet,
    DepartamentoViewSet
)

router = routers.SimpleRouter()
router.register(r'provider', ProviderViewSet)
router.register(r'departamento', DepartamentoViewSet)
router.register(r'vendor', VendorListViewSet)
router.register(r'vendors', VendorAllListViewSet)

urlpatterns = [
    #url para applications
    url(r'^api/', include(router.urls)),

]
