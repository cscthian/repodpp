from django.conf.urls import url
from . import views, viewsets

urlpatterns = [
    #urls para servicios
    url(
        r'^api/administrador/ventas/$',
        viewsets.VentasViewSet.as_view({'get': 'list'}),
        name='admin-ventas'
    ),
    url(
        r'^api/nota/items/(?P<guide>[-\w]+)/$',
        viewsets.NotaItem.as_view({'get': 'list'}),
        name='admin-nota_item'
    ),
    url(
        r'^api/control/diarios/$',
        viewsets.LostMagazineListViewSet.as_view({'get': 'list'}),
        name='control-list_lost'
    ),
    url(
        r'^api/save/diairios/perdidos/$',
        viewsets.AddLostMagazineViewSet.as_view({'post': 'create'}),
        name='control-lost_add'
    ),
    url(
        r'^api/save/diairios/perdidos/close/$',
        viewsets.RinicioCuentaViewSet.as_view({'post': 'create'}),
        name='control-lost_close'
    ),
    #urls paara servicios contabilidad
    url(
        r'^api/boleta/items/(?P<date>[-\w]+)/(?P<date2>[-\w]+)/$',
        viewsets.ListProdBoleta.as_view({'get': 'list'}),
        name='contabilidad-list-item'
    ),
    url(
        r'^api/boleta/emitidos/(?P<date1>[-\w]+)/(?P<date2>[-\w]+)/$',
        viewsets.ListBoletaEmitida.as_view({'get': 'list'}),
        name='contabilidad-list-emitidos'
    ),
    url(
        r'^api/save/boleta/$',
        viewsets.AddBoletaViewSet.as_view({'post': 'create'}),
        name='contabilidad-add_boleta'
    ),
    #urls para vistas
    url(
        r'^panel/administrador$',
        views.PanelAdmin.as_view(),
        name='home-admin'
    ),
    url(
        r'^guia/nota-credito/$',
        views.NotaCreditoView.as_view(),
        name='admin-nota'
    ),
    #urls para control
    url(
        r'^panel/control$',
        views.PanelControl.as_view(),
        name='home-control'
    ),
    #urls para administrador
    url(
        r'^contabilidad/lista-productos$',
        views.ProductosBoleta.as_view(),
        name='contabilidad-list'
    ),
    url(
        r'^contabilidad/emitidos$',
        views.BoletasEmitidas.as_view(),
        name='contabilidad-emitidos'
    ),
    url(
        r'^contabilidad/detalle-boleta/(?P<pk>\d+)/$',
        views.BoletasDetailView.as_view(),
        name='contabilidad-detalle_boleta'
    ),
    url(
        r'^admin/control/add$',
        views.ControlMagazins.as_view(),
        name='control-add'
    ),
    url(
        r'^admin/control/list$',
        views.ControlMagazinsList.as_view(),
        name='control-list'
    ),
    url(
        r'^admin/control/delete/(?P<pk>\d+)/$',
        views.LostMagazineDeleteView.as_view(),
        name='control-delete'
    ),
]
