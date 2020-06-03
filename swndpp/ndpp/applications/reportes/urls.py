from django.conf.urls import url, include
from . import views

urlpatterns = [
    #url para home de la aplicacion
    url(
        r'^buscar-guia/$',
        views.SearchGuide.as_view(),
        name='reporte-search_guide'
    ),
    #url para buscar factura por numero
    url(
        r'^buscar-factura/$',
        views.SearchVoucher.as_view(),
        name='reporte-search_voucher'
    ),
    # url para agregar factura
    url(
        r'^agregar-comprobante/$',
        views.VoucherCreateView.as_view(),
        name='add-voucher'
    ),
    # url para modificar factura
    url(
        r'^ver-factura/(?P<pk>\d+)/$',
        views.VoucherUpdateView.as_view(),
        name='update-voucher'
    ),
    #url para anular faactura
    url(
        r'^eliminar-comprobante/(?P<pk>\d+)/$',
        views.VoucherDeleteView.as_view(),
        name='delete-voucher'
    ),
    #agregar nota de credito de una factura
    url(
        r'^agregar-nota-credito/(?P<pk>\d+)/$',
        views.NotaCreditoCreateView.as_view(),
        name='add-nota_credito'
    ),
    #url para anular nota de credito
    url(
        r'^eliminar-nota-de-credito/(?P<pk>\d+)/$',
        views.NotaCreditoDeleteView.as_view(),
        name='delete-nota_credito'
    ),
    # url para ver facturas sin nota de credito
    url(
        r'^voucher/factura-sin-credito/$',
        views.FacturaSinCredito.as_view(),
        name='voucher_sin-credito'
    ),





    #rest de aplicacion reportes
    url(r'^', include('applications.reportes.url_services', namespace="reportes_servis_url")),
]
