# -*- encoding: utf-8 -*-
from django.conf.urls import url
from . import views, viewsets

urlpatterns = [
    #urls para servicios
    url(
        r'^api/ventas/cierre/$',
        viewsets.CierreMesViewSet.as_view({'get': 'list'}),
        name='api-cierre'
    ),
    url(
        r'^api/ventas/cierre/venta-neta/$',
        viewsets.VentanetaViewSet.as_view({'get': 'list'}),
        name='api-venta_neta'
    ),
    url(
        r'^api/ventas/cierre/ingreso-neto/$',
        viewsets.IngresonetoViewSet.as_view({'get': 'list'}),
        name='api-ingreso-neto'
    ),
    url(
        r'^api/reportes/diario/(?P<fecha1>[-\w]+)/(?P<fecha2>[-\w]+)/(?P<tipo>[-\w]+)/$',
        viewsets.RankinMagazineSet.as_view({'get': 'list'}),
        name='reportes-magazine'
    ),
    url(
        r'^api/reportes/canillas/lista/(?P<pk>[-\w]+)/$',
        viewsets.RankingVendorSet.as_view({'get': 'list'}),
        name='reportes-canillas'
    ),
    url(
        r'^api/reportes/canillas/historial/$',
        viewsets.HistoriaVenderSet.as_view({'get': 'list'}),
        name='reportes-historial'
    ),
    url(
        r'^api/reportes/canilla/cero/(?P<pk>[-\w]+)/$',
        viewsets.CeroVenderSet.as_view({'get': 'list'}),
        name='reportes-cero'
    ),
    url(
        r'^api/reportes/guia/lista/(?P<numero>[-\w]+)/$',
        viewsets.HistoryGuideViewset.as_view({'get': 'list'}),
        name='reportes-guia'
    ),
    url(
        r'^api/reportes/detalle-guia/(?P<pk>[-\w]+)/$',
        viewsets.DetailHistoryGuideViewset.as_view({'get': 'list'}),
        name='reportes-guia_detalle'
    ),
    url(
        r'^api/reportes/estado-guia/(?P<date1>[-\w]+)/(?P<date2>[-\w]+)/$',
        viewsets.StateGuideViewset.as_view({'get': 'list'}),
        name='reportes-guia_estado'
    ),
    url(
        r'^api/reportes/resumen-guia/(?P<date1>[-\w]+)/(?P<date2>[-\w]+)/$',
        viewsets.ResumenReportGuideViewset.as_view({'get': 'list'}),
        name='reportes-guia_resumen'
    ),
    url(
        r'^api/reporte/guia/count-real/save/$',
        viewsets.RegisterRealCountViewSet.as_view({'post': 'create'}),
        name='reporte-guia_real_count'
    ),
    #urls para vistas
    url(
        r'^reportes/ventas/neta/$',
        views.VentaNetaView.as_view(),
        name='ventas-neta'
    ),
    url(
        r'^reportes/ventas/margen-ganacia/$',
        views.MargenView.as_view(),
        name='ventas-margen'
    ),
    url(
        r'^reportes/cierre/add/$',
        views.CierreCreateView.as_view(),
        name='cierre-add'
    ),
    url(
        r'^reportes/cierre/list/$',
        views.CierreMesListView.as_view(),
        name='cierre-list'
    ),
    url(
        r'^reportes/cierre/delete/(?P<pk>\d+)/$',
        views.CierreMesDeleteView.as_view(),
        name='cierre-delete'
    ),
    url(
        r'^reportes/diarios/report/$',
        views.DiariosReport.as_view(),
        name='diarios-report'
    ),
    url(
        r'^reportes/productos/report/$',
        views.ProductReport.as_view(),
        name='product-report'
    ),
    url(
        r'^reportes/vendedores/report/$',
        views.VendorReport.as_view(),
        name='vendor-report'
    ),
    url(
        r'^reportes/vendedores/tope/$',
        views.VendorTopeReport.as_view(),
        name='vendor-tope'
    ),
    url(
        r'^reportes/vendedores/historial/$',
        views.VendorHistoriaReport.as_view(),
        name='vendor-historial'
    ),
    url(
        r'^reportes/vendedores/canilla-cero/$',
        views.VendorCeroReport.as_view(),
        name='vendor-cero'
    ),
    url(
        r'^reportes/almacen/missing$',
        views.MagazineMissingReport.as_view(),
        name='almacen-missing'
    ),
    url(
        r'^reportes/control/guias-culminadas$',
        views.ControlGuidesReport.as_view(),
        name='control-guias'
    ),
    url(
        r'^reportes/guias-panel$',
        views.GuidesReport.as_view(),
        name='reporte-guias'
    ),
    url(
        r'^reportes/guias-items/(?P<pk>\d+)/$',
        views.GuidesItemReport.as_view(),
        name='reporte-guias_item'
    ),
    url(
        r'^reportes/guias-items-detalle/(?P<pk>\d+)/$',
        views.GuidesItemDetalleReport.as_view(),
        name='reporte-guias_item_detalle'
    ),
    url(
        r'^reportes/guias-estado/$',
        views.GuideEstadoReport.as_view(),
        name='reporte-guias_estado'
    ),
    url(
        r'^reportes/guias-resumen/$',
        views.GuideResumenReport.as_view(),
        name='reporte-guias_resumen'
    ),
]
