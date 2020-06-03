from django.conf.urls import url, include
from . import views, viewsets
from .models import Guide, DetailGuide
from rest_framework import routers
from .viewsets import (
    MagazineDayViewSet,
    GuideViewSet,
    MagazineViewSet,
    GuideListViewSet,
    DetailGuideViewSet,
    DGdeleteViewSet,
    DGcreateViewSet,
)

router = routers.SimpleRouter()
router.register(r'magazin', MagazineViewSet)
router.register(r'magazine', MagazineDayViewSet)
#router.register(r'save/guide', GuideViewSet, base_name=Guide)
router.register(r'save/detail/guide', DGcreateViewSet, base_name=DetailGuide)

urlpatterns = [
    #url para applications
    url(r'^api/', include(router.urls)),

    url(
        r'^api/guides/(?P<date1>[-\w]+)/(?P<date2>[-\w]+)/$',
        viewsets.GuideListViewSet.as_view({'get': 'list'}),
        name='guide-list_date'
    ),
    url(
        r'^api/save/guide/add/$',
        viewsets.GuideViewSet.as_view({'post': 'create'}),
        name='guide-api_save'
    ),
    url(
        r'^api/producto/retrive/(?P<pk>[-\w]+)/$',
        viewsets.ProdViewSet.as_view({'get': 'retrieve'}),
        name='magazine-prod_retrive'
    ),
    url(
        r'^api/update/guide/(?P<pk>[-\w]+)/$',
        viewsets.DetailGuideViewSet.as_view({'get': 'list'}),
        name='guide-items'
    ),
    url(
        r'^api/guide/detail/delete/(?P<guia>[-\w]+)/$',
        viewsets.DGdeleteViewSet.as_view({'post': 'destroy'}),
        name='guide_detail-delete'
    ),
    url(
        r'^api/guide-detalle/list-asignar/$',
        viewsets.DetailGuideListViewSet.as_view({'get': 'list'}),
        name='guide_detail-items'
    ),
    url(
        r'^api/detail_guide/retrive/(?P<pk>[-\w]+)/$',
        viewsets.DetailGuideGetViewSet.as_view({'get': 'retrieve'}),
        name='magazine-detail_guide_retrive'
    ),
    url(
        r'^api/guide-detalle/sin-culminar/$',
        viewsets.ListDetailGuideViewSet.as_view({'get': 'list'}),
        name='guide_detail-sin_culminar'
    ),
    url(
        r'^api/guide-detalle/lista-tipo/(?P<tipo>[-\w]+)/$',
        viewsets.ListDetailGuideTipoViewSet.as_view({'get': 'list'}),
        name='guide_detail-por_tipo'
    ),
    url(
        r'^api/guides/culmined/(?P<date1>[-\w]+)/(?P<date2>[-\w]+)/$',
        viewsets.GuideListCulminedViewSet.as_view({'get': 'list'}),
        name='guide__culmined'
    ),
    url(
    #urls para magazine
        r'^almacen/recepcion/Diario/add/$',
        views.MagazineCreate.as_view(),
        name='magazine-add'
    ),
    url(
        r'^almacen/recepcion/producto/add/$',
        views.ProductCreate.as_view(),
        name='magazine-add_prod'
    ),
    url(
        r'^almacen/recepcion/producto/add/plantilla/(?P<pk>\d+)/$',
        views.ProductCreatePlantillaView.as_view(),
        name='magazine-prod_plantilla'
    ),
    url(
        r'^almacen/recepcion/Diario/day/list/(?P<pk>\d+)/(?P<tipo>\d+)/$',
        views.DaysTemplateView.as_view(),
        name='magazine-list_day'
    ),
    url(
        r'^almacen/recepcion/Diario/update/(?P<day>\d+)/(?P<pk>\d+)/(?P<tipo>\d+)/$',
        views.MagazineUpdateView.as_view(),
        name='magazine-update'
    ),
    url(
        r'^almacen/recepcion/Diario/update/(?P<pk>\d+)/(?P<tipo>\d+)/$',
        views.ProductUpdateView.as_view(),
        name='magazine-update-prod'
    ),
    url(
        r'^almacen/recepcion/Diario/delete/(?P<pk>\d+)/$',
        views.MagazineDeleteView.as_view(),
        name='magazine-delete'
    ),
    url(
        r'^almacen/recepcion/Diario/list/$',
        views.MagazineListView.as_view(),
        name='magazine-list'
    ),
    url(
        r'^api/productos/por-cobrar/(?P<date>[-\w]+)/$',
        viewsets.ProductosPorCobrar.as_view({'get': 'list'}),
        name='productos-por_cobrar'
    ),
    url(
    #urls para diario
        r'^almacen/recepcion/guide/add/$',
        views.GuideRegisterView.as_view(),
        name='guide-add'
    ),
    url(
        r'^almacen/recepcion/guide/list/$',
        views.GuideListView.as_view(),
        name='guide-list'
    ),
    url(
        r'^almacen/recepcion/guide/update/(?P<pk>\d+)/$',
        views.GuideUpdateView.as_view(),
        name='guide-update'
    ),
    url(
        r'^almacen/recepcion/guide/detail/(?P<pk>\d+)/$',
        views.GuideDetailView.as_view(),
        name='guide-detail'
    ),
    url(
        r'^almacen/recepcion/guide/delete/(?P<pk>\d+)/$',
        views.GuideDeleteView.as_view(),
        name='guide-delete'
    ),
    url(
        #urls para guia detalle
        r'^almacen/recepcion/guide/detail/update/(?P<pk>\d+)/$',
        views.DetailGuideUpdateView.as_view(),
        name='detail_guide-update'
    ),
    url(
        r'^almacen/recepcion/guide/detail/delete/(?P<pk>\d+)/$',
        views.DetailGuideDeleteView.as_view(),
        name='detail_guide-delete'
    ),
    url(
        r'^almacen/productos/por-cobrar/$',
        views.ProducPorCobrarView.as_view(),
        name='magazine-prod_por_cobrar'
    ),
]
