# -*- encoding: utf-8 -*-
from django.conf.urls import url
from . import views, viewsets
from .viewsets import MovimientosViewSet, PagoscreateViewSet

urlpatterns = [
    #urls para servicios
    url(
        r'^api/pagos/movimientos/(?P<pk>[-\w]+)/$',
        viewsets.MovimientosViewSet.as_view({'get': 'list'}),
        name='pagos-movimientos'
    ),
    url(
        r'^api/pagos/save/(?P<pk>[-\w]+)/$',
        viewsets.PagoscreateViewSet.as_view({'post': 'create'}),
        name='pagos-add'
    ),
    url(
        r'^api/ventas/save/$',
        viewsets.VentacreateViewSet.as_view({'post': 'create'}),
        name='pagos-venta_add'
    ),
    url(
        r'^api/pagos/ca1ja/cudrar/liquidacion/$',
        viewsets.CuadrarCajaViewSet.as_view({'get': 'list'}),
        name='pagos-reporte_liquidacion'
    ),
    url(
        r'^api/pagos/lista-productos-venta/$',
        viewsets.ProdVentaViewSet.as_view({'get': 'list'}),
        name='pagos-prod_venta'
    ),
    #urls para caja
    url(
        r'^caja/cobros/cobrar/cobros$',
        views.CobrosView.as_view(),
        name='pagos-cobrar'
    ),
    url(
        r'^caja/cobros/cobrar/anular/(?P<pk>\d+)/$',
        views.PaymentDeleteView.as_view(),
        name='pagos-anular'
    ),
    #urls para cuadrar caja
    url(
        r'^caja/cobros/cuadrar/caja/$',
        views.CuadrarCajaView.as_view(),
        name='pagos-cudarar'
    ),
    url(
        r'^caja/cobros/cobrar/cuadrar/detalle/(?P<pk>\d+)/$',
        views.DetalleCuadrarView.as_view(),
        name='pagos-detalle-cuadrar'
    ),
    url(
        r'^caja/cobros/cuadrar/confirmar/$',
        views.ConfirmarView.as_view(),
        name='pagos-confirmar'
    ),
    url(
        r'^caja/ventas/list/$',
        views.VentasListView.as_view(),
        name='venta-list'
    ),
    url(
        r'^caja/ventas/delete/(?P<pk>\d+)/$',
        views.VentaDeleteView.as_view(),
        name='venta-delete'
    ),
    #urls para cuadrar devoluciones
    url(
        r'^caja/cobros/reportes/devolucion$',
        views.DevolucionListView.as_view(),
        name='pagos-devoluciones'
    ),
    url(
        r'^caja/cobros/cobrar/devolucion/detalle/(?P<pk>\d+)/$',
        views.DetalleDevolucion.as_view(),
        name='pagos-detalle-devolucion'
    ),
    #urls para reportes
    url(
        r'^caja/cobros/reportes/deudores$',
        views.FaltantesView.as_view(),
        name='pagos-faltantes'
    ),
    url(
        r'^caja/cobros/reportes/anulados$',
        views.InvoceAnulados.as_view(),
        name='pagos-anulados'
    ),
    url(
        r'^caja/cobros/reportes/anulado/detalle/(?P<pk>\d+)/$',
        views.DetalleAnulado.as_view(),
        name='pagos-anulado-detalle'
    ),
    url(
        r'^caja/cobros/cuadrar/reporte/$',
        views.CuadrarReporteView.as_view(),
        name='pagos-cuadrar_reporte'
    ),
    url(
        r'^caja/cobros/reporte/devoluciones$',
        views.DevolucionReporteView.as_view(),
        name='pagos-devolucion_reporte'
    ),
    url(
        r'^caja/cobros/venta-tienda/$',
        views.VentaTiendaView.as_view(),
        name='pagos-tienda'
    ),
    url(
        r'^caja/reportes/guias-pendientes/$',
        views.GuiasPendientesListView.as_view(),
        name='guias-pendientes'
    ),
    url(
        r'^caja/reportes/guias-pendientes/deuda/(?P<pk>\d+)/$',
        views.DetalleGuiasPendientesListView.as_view(),
        name='guias-pendientes-detalle'
    ),

]
