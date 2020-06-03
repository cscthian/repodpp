# django
from django.conf.urls import url

# local
from . import viewsets


urlpatterns = [
    #recuperar movimientos de guia
    url(
        r'^api/pagos/movimientos/(?P<cod>[-\w]+)/$',
        viewsets.MovimientosGuideViewSet.as_view({'get': 'list'}),
        name='pagos-movimientos'
    ),
    url(
        r'^api/pagos/save/(?P<pk>[-\w]+)/$',
        viewsets.PagoscreateViewSet.as_view({'post': 'create'}),
        name='pagos-add'
    ),
]
