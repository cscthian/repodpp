# django
from django.conf.urls import url

# local
from . import viewsets


urlpatterns = [
    #agregar Unidad de negocio
    url(
        r'^api/factura/list/$',
        viewsets.ListFacturaViewSet.as_view({'get': 'list'}),
        name='admin_api-factura_list'
    ),
    url(
        r'^api/save/pago-factura/$',
        viewsets.PagoFacturaViewSet.as_view({'post': 'create'}),
        name='admin_api-factura_pago'
    ),
    url(
        r'^api/emitir-boleta/(?P<date>[-\w]+)/(?P<rs>[-\w]+)/(?P<dep>[-\w]+)/$',
        viewsets.EmitirBoletaViewSet.as_view({'get': 'list'}),
        name='admin-emitir_boleta'
    ),
    url(
        r'^api/save/boleta/$',
        viewsets.AddBoletaViewSet.as_view({'post': 'create'}),
        name='admin_api-nueva_boleta'
    ),
    #url para cuadrar venta en fechas
    url(
        r'^api/cuadre-ventas/(?P<date1>[-\w]+)/(?P<date2>[-\w]+)/$',
        viewsets.CuadreVentaViewSet.as_view({'get': 'list'}),
        name='admin_api-cuadre_venta'
    ),
    #url para perdida o montos flatates
    url(
        r'^api/montos-faltantes/$',
        viewsets.MontosFaltantesViewSet.as_view({'get': 'list'}),
        name='admin_api-montos_faltantes'
    ),
    #url para saldar perdida
    url(
        r'^api/save/montos-faltantes/$',
        viewsets.ResetMontosFaltantesViewSet.as_view({'post': 'create'}),
        name='admin_api-saldar_faltantes'
    ),
    #url para compra total
    url(
        r'^api/reportes/ventas/compra-total/(?P<pro>[-\w]+)/(?P<rs>[-\w]+)/(?P<dep>[-\w]+)/$',
        viewsets.LiquidacionProveedorReporteVieset.as_view({'get': 'list'}),
        name='admin-ventas_compra_total'
    ),
    #url para compra facturada
    url(
        r'^api/reportes/ventas/compra-facturada/(?P<pro>[-\w]+)/(?P<rs>[-\w]+)/(?P<dep>[-\w]+)/(?P<date>[-\w]+)/$',
        viewsets.LiquidacionFacturaProveedorReporteVieset.as_view({'get': 'list'}),
        name='admin-ventas_compra_facturada'
    ),
]
