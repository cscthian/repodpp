# -*- encoding: utf-8 -*-
from django.conf.urls import url
from . import views, viewsets

urlpatterns = [
    #urls para servicios
    url(
        r'^api/caja/movimientos/(?P<fecha>[-\w]+)/$',
        viewsets.MovimientosCaja.as_view({'get': 'list'}),
        name='liquidacion-caja_movimientos'
    ),
    url(
        r'^api/caja/liuidar/guia/(?P<fecha1>[-\w]+)/(?P<fecha2>[-\w]+)/(?P<prov>[-\w]+)/$',
        viewsets.LiquidacionGuia.as_view({'get': 'list'}),
        name='liquidacion-rango'
    ),
    url(
        r'^api/liquidacion/detalle/(?P<fecha1>[-\w]+)/(?P<fecha2>[-\w]+)/$',
        viewsets.LiquidacionGuiaDetalle.as_view({'get': 'list'}),
        name='liquidacion-guia_detalle'
    ),
    url(
        r'^api/caja/liuidacion/dia/(?P<fecha>[-\w]+)/$',
        viewsets.LiquidacionCaja.as_view({'get': 'list'}),
        name='liquidacion-caja'
    ),
    url(
        r'^api/caja/liuidacion-proveedor/(?P<fecha>[-\w]+)/$',
        viewsets.LiquidacionProveedorView.as_view({'get': 'list'}),
        name='liquidacion-proveedor_dia'
    ),
    #urls para vistas
    url(
        r'^movimientos/pagos/caja/liuidar/$',
        views.LiquidacionDiariaView.as_view(),
        name='liquidacion'
    ),
    url(
        r'^movimientos/pagos/caja/liuidar-por-proveedor/$',
        views.LiquidacionDiariaProvidorView.as_view(),
        name='liquidacion-por_proveedor'
    ),
    url(
        r'^movimientos/liquidacion/guias/$',
        views.LiquidacionGuiaView.as_view(),
        name='liquidacion-guia'
    ),
    url(
        r'^caja/movimientos-caja/$',
        views.MovimientosCajaView.as_view(),
        name='liquidacion-deudas_vendor'
    ),
    url(
        r'^caja/liquidacion/provider/$',
        views.LiquidacionProviderView.as_view(),
        name='liquidacion-provider_day'
    ),
]
