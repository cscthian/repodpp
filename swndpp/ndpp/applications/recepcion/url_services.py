# django
from django.conf.urls import url

# local
from . import viewsets


urlpatterns = [
    #agregar Unidad de negocio
    url(
        r'^api/magazine/list/$',
        viewsets.MagazineListViewSet.as_view({'get': 'list'}),
        name='recepcion_api-magazine_list'
    ),
    #url para listar magazine day
    url(
        r'^api/magazine-day/list/$',
        viewsets.MagazineDayViewSet.as_view({'get': 'list'}),
        name='recepcion_api-magazineday_list'
    ),
    #url para agregar guias nuevas
    url(
        r'^api/save/guide/add/$',
        viewsets.GuideAddViewSet.as_view({'post': 'create'}),
        name='guide-api_save'
    ),
    #url para recuperar un producto
    url(
        r'^api/producto/retrive/(?P<pk>[-\w]+)/$',
        viewsets.ProdViewSet.as_view({'get': 'retrieve'}),
        name='magazine-prod_retrive'
    ),
]
