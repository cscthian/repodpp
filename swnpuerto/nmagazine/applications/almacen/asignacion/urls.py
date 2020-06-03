# -*- encoding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework import routers

from . import views, viewsets

from applications.almacen.recepcion.models import DetailGuide

from .models import DetailAsignation
from .viewsets import(
    DetailAsignationViewSet,
    DACreateViewSet,
    GenerarPautaDinamica,
    AsignationListViewSet,
    ConsultaViewSet,
)

router = routers.SimpleRouter()
router.register(
    r'lista/pauta',
    DetailAsignationViewSet,
    base_name=DetailAsignation
)
router.register(
    r'save/asignacion',
    DACreateViewSet,
    base_name=DetailAsignation,
)

urlpatterns = [
    #url para las api de asignacion
    url(r'^api/', include(router.urls)),
    url(
        r'^api/asignations/(?P<date1>[-\w]+)/(?P<date2>[-\w]+)/$',
        viewsets.AsignationListViewSet.as_view({'get': 'list'}),
        name='asignations-list'
    ),
    url(
        r'^api/pautas/(?P<pk>[-\w]+)/$',
        viewsets.DetailAsignationViewSet.as_view({'get': 'list'}),
        name='pautas'
    ),
    url(
        r'^api/pautas/dinamica/generar/(?P<dia>[-\w]+)/$',
        viewsets.GenerarPautaDinamica.as_view({'get': 'list'}),
        name='pautas-dinamica'
    ),
    url(
        r'^almacen/entrada/pautas/dinamica/generar/$',
        views.PautaDinamicaView.as_view(),
        name='entrada-pauta_dinamica'
    ),
    url(
        r'^api/asignacion/save/(?P<pk>[-\w]+)/$',
        viewsets.DACreateViewSet.as_view({'post': 'create'}),
        name='asignacion'
    ),
    url(
        r'^api/asignacion/producto-save/(?P<cod>[-\w]+)/(?P<dni>[-\w]+)/$',
        viewsets.RegisterEntregaProdView.as_view({'post': 'create'}),
        name='asignacion-prod_add'
    ),
    url(
        r'^api/pauta/save/(?P<pk>[-\w]+)/$',
        viewsets.RegisterPautaView.as_view({'post': 'create'}),
        name='pauta'
    ),
    url(
        r'^api/entrega/lista/(?P<tipo>[-\w]+)/$',
        viewsets.DetailAsignationListViewSet.as_view({'get': 'list'}),
        name='entrega-lista_entregas'
    ),
    url(
        r'^api/asignacion/consulta/(?P<pk>[-\w]+)/$',
        viewsets.ConsultaViewSet.as_view({'get': 'list'}),
        name='entrega-consulta'
    ),
    url(
        r'^api/pautas/modificar/(?P<pk>[-\w]+)/$',
        viewsets.UpdateAsignationViewSet.as_view({'get': 'list'}),
        name='entrega-update'
    ),
    url(
        r'^api/pauta/update/(?P<pk>[-\w]+)/$',
        viewsets.UpdatePautaView.as_view({'get': 'list'}),
        name='pauta-update'
    ),
    url(
        r'^api/pauta/cargar-entrega/(?P<cod>[-\w]+)/(?P<pk>[-\w]+)/$',
        viewsets.CargarPautaView.as_view({'get': 'list'}),
        name='pauta-cargar'
    ),
    url(
        r'^api/pauta/habilitar/(?P<pk>[-\w]+)/$',
        viewsets.EnabledPautaView.as_view({'post': 'create'}),
        name='pauta-enabled'
    ),
    #############url para vistas de asigancion############3
    url(
        r'^reception/almacen/entregas/list/(?P<pk>\d+)/$',
        views.MagazineDeliverListView.as_view(),
        name='entrega-list'
    ),
    url(
        r'^reception/almacen/entrega-magazine/listar-items$',
        views.MagazineListDeliverView.as_view(),
        name='entrega-list_magazzine'
    ),
    url(
        r'^reception/almacen/entregas/producto/list/$',
        views.ProductDeliverListView.as_view(),
        name='entrega-list-prod'
    ),
    url(
        r'^almacen/recepcion/entrega/registro/(?P<key>\d+)/(?P<pk>\d+)/$',
        views.DetailGuideDetailView.as_view(),
        name='entrega-add'
    ),
    url(
        r'^almacen/recepcion/producto/entrega/registro/(?P<key>\d+)/(?P<pk>\d+)/$',
        views.ProdDetailGuideDetailView.as_view(),
        name='entrega-add_producto'
    ),
    url(
        r'^almacen/recepcion/pauta/registro/(?P<pk>\d+)/$',
        views.PautaDeliverView.as_view(),
        name='pauta-add'
    ),
    url(
        r'^almacen/recepcion/consulta/lista/$',
        views.ListaConsultaView.as_view(),
        name='entrega-list-consulta'
    ),
    url(
        r'^almacen/recepcion/consulta/ver/(?P<pk>\d+)/$',
        views.DetailConsultaView.as_view(),
        name='consulta-view'
    ),
    url(
        r'^almacen/registrar/entrega-producto/$',
        views.AddEntregaProducto.as_view(),
        name='entrega-prod_add'
    ),
    url(
        r'^entrega/list-producto-delete/(?P<cod>\d+)/(?P<tipo>\d+)/$',
        views.PautaDeleteListView.as_view(),
        name='entrega-pauta_list_delete'
    ),
    url(
        r'^entrega/producto-delete/(?P<pk>\d+)/$',
        views.PautaDeleteView.as_view(),
        name='entrega-pauta_delete'
    ),
    #entreg productos por dni
    url(
        r'^entrega/diario/pauta-diario/(?P<pk>\d+)/$',
        views.PautaDiarioView.as_view(),
        name='pauta-diario'
    ),
    url(
        r'^almacen/registrar/entrega-diario/$',
        views.AddEntregaDiario.as_view(),
        name='entrega-diario_dni'
    ),
]
