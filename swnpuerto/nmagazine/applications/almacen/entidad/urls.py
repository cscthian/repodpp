# -*- encoding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework import routers
from . import views

from .viewsets import ProviderViewSet, VendorListViewSet, VendorAllListViewSet

router = routers.SimpleRouter()
router.register(r'provider', ProviderViewSet)
router.register(r'vendor', VendorListViewSet)
router.register(r'vendors', VendorAllListViewSet)

urlpatterns = [
    #url para applications
    url(r'^api/', include(router.urls)),
    url(
    #urls para Proveedor
        r'^almacen/entidad/proveedor/add/$',
        views.ProviderCreateView.as_view(),
        name='provider-add'
    ),
    url(
        r'^almacen/entidad/proveedor/update/(?P<pk>\d+)/$',
        views.ProviderUpdateView.as_view(),
        name='provider-update'
    ),
    url(
        r'^almacen/entidad/proveedor/delete/(?P<pk>\d+)/$',
        views.ProviderDeleteView.as_view(),
        name='provider-delete'
    ),
    url(
        r'^almacen/entidad/proveedor/detail/(?P<pk>\d+)/$',
        views.ProviderDetailView.as_view(),
        name='provider-detail'
    ),
    url(
        r'^almacen/entidad/proveedor/lista/$',
        views.ProviderListView.as_view(),
        name='provider-list'
    ),
    url(
    #urls para canillas
        r'^almacen/entidad/canilla/lista/$',
        views.VendorListView.as_view(),
        name='vendor-list'
    ),
    url(
    #urls para canillas
        r'^almacen/entidad/canilla/add/$',
        views.VendorCreateView.as_view(),
        name='vendor-add'
    ),
    url(
    #urls para canillas
        r'^almacen/entidad/canilla/update/(?P<pk>\d+)/$',
        views.VendorUpdateView.as_view(),
        name='vendor-update'
    ),
    url(
    #urls para canillas
        r'^almacen/entidad/canilla/delete/(?P<pk>\d+)/$',
        views.VendorDeleteView.as_view(),
        name='vendor-delete'
    ),
    url(
    #urls para canillas
        r'^almacen/entidad/canilla/disable/(?P<pk>\d+)/$',
        views.VendorDisbleView.as_view(),
        name='vendor-disable'
    ),
    url(
    #urls para canillas
        r'^almacen/entidad/canilla/enabled/(?P<pk>\d+)/$',
        views.VendorEnabledView.as_view(),
        name='vendor-enabled'
    ),
    url(
    #urls para canillas
        r'^almacen/entidad/canilla/detail/(?P<pk>\d+)/$',
        views.VendorDetailView.as_view(),
        name='vendor-detail'
    ),
    url(
    #urls para entidad
        r'^correr-scrip/(?P<pk>\d+)/$',
        views.ScripTemplateView.as_view(),
        name='scrip-correr'
    ),
]
