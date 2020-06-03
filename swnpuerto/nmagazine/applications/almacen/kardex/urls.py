from django.conf.urls import url, include
from rest_framework import routers
from . import views, viewsets

urlpatterns = [
    #url para api
    url(
        r'^api/kardex/inventario/$',
        viewsets.InventarioListViewSet.as_view({'get': 'list'}),
        name='inventario-lista'
    ),
    url(
        r'^api/kardex/constatar/(?P<guide>[-\w]+)/$',
        viewsets.ConstatarListViewSet.as_view({'get': 'list'}),
        name='constatar'
    ),
    url(
        r'^api/kardex/inventario/dealle/(?P<guide>[-\w]+)/$',
        viewsets.DetalleViewSet.as_view({'get': 'list'}),
        name='inventario-detalle'
    ),
    url(
        r'^api/kardex/constatar/save$',
        viewsets.ConstatarCreateView.as_view({'post': 'create'}),
        name='constatar-save'
    ),
    #urls para las vistass
    url(
        r'^almacen/kardex/guide/kardex/$',
        views.KardexTemplateView.as_view(),
        name='guide-kardex'
    ),
    url(
        r'^almacen/kardex/constatar/$',
        views.ConstatarView.as_view(),
        name='guide-constatar'
    ),
    url(
        r'^almacen/kardex/detalle/(?P<pk>\d+)/$',
        views.DetalleInventarioView.as_view(),
        name='guide-detalle'
    ),
    url(
        r'^almacen/kardex/productos-almacen/$',
        views.MagazineEnAlmacenView.as_view(),
        name='guide-en_alamcen'
    ),
]
