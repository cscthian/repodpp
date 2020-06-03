from django.conf.urls import url, include
from . import views

urlpatterns = [
    #url para home de reporte
    url(
        r'^administracion/reportes/$',
        views.AdministracionReporte.as_view(),
        name='administracion-reporte_index'
    ),
    #url para lista de guias en reportes administracion
    url(
        r'^administracion/reportes/guia-lista/$',
        views.ListaGuiaReporte.as_view(),
        name='administracion-reporte_guia-lista'
    ),
    #url para lista de facturas - reporte control facturas
    url(
        r'^administracion/reportes/factura-lista/$',
        views.ListaFacturaReporte.as_view(),
        name='administracion-reporte_factura-lista'
    ),
    #url para liquidacion proveedor
    url(
        r'^administracion/reportes/liquidacion-proveedor/$',
        views.LiquidacionProveedorReporte.as_view(),
        name='administracion-reporte_liquidacion_proveedor'
    ),
    #url para liquidacion por facturra
    url(
        r'^administracion/reportes/liquidacion-proveedor-factura/$',
        views.LiquidacionFacturaProveedorReporte.as_view(),
        name='administracion-reporte_liquidacion_proveedor_factura'
    ),
    #url para agregar pagos de facturas
    url(
        r'^administracion/procesos/registra-pago-factura/$',
        views.LiquidacionRegistrarPagoReporte.as_view(),
        name='administracion-proceso_pagos_factura'
    ),
    #url para ver seguimiento de agentes
    url(
        r'^administracion/reporte/seguimiento-agentes/$',
        views.SeguimientoAgentesView.as_view(),
        name='administracion-seguimiento_agentes'
    ),
    #url para ver deudas de agente
    url(
        r'^administracion/reporte/deuda-agente/(?P<codigo>[-\w]+)/$',
        views.DeudaByAgentesView.as_view(),
        name='administracion-deuda_agentes'
    ),

    #url para emitir boleta de pago
    url(
        r'^administracion/procesos/emitir-boleta/$',
        views.EmitirBoletaView.as_view(),
        name='administracion-emitir_boleta'
    ),
    #url para reporte de ventas por fecha
    url(
        r'^administracion/reportes/ventas/por-fecha/$',
        views.CuadreVentasView.as_view(),
        name='administracion-ventas_por_fecha'
    ),
    #
    url(
        r'^administracion/reportes/faltantes/$',
        views.MontosFaltantesView.as_view(),
        name='administracion-reporte_faltantes'
    ),
    #
    url(
        r'^administracion/procesos/boletas-emitidas/$',
        views.ListaBoletasEmitidas.as_view(),
        name='administracion-proceso_boletas_emitidas'
    ),
    #
    url(
        r'^administracion/procesos/boleta-eliminar/(?P<pk>\d+)/$',
        views.DeleteBoletasEmitida.as_view(),
        name='administracion-proceso_boletas_eliminar'
    ),
    #url para pantalla buscar guias
    url(
        r'^administracion/reportes/buscar/$',
        views.SearchGuidesView.as_view(),
        name='administracion-reporte_buscar-guia'
    ),
    #url para ver el historial de una guia
    url(
        r'^administracion/reportes/history/(?P<pk>\d+)/$',
        views.HistoryGuidesView.as_view(),
        name='administracion-reporte_history-guia'
    ),


    #rest de aplicacion adminisracion
    url(r'^', include('applications.administracion.url_services', namespace="adminisracion_servis_url")),
]
