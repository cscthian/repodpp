# django
from django.conf.urls import url

# local
from . import viewsets


urlpatterns = [
    #agregar Unidad de negocio
    url(
        r'^api/save-guide/voucher/$',
        viewsets.VoucherGuideAddViewSet.as_view({'post': 'create'}),
        name='reportes_api-add_guides'
    ),
    url(
        r'^api/delete-guide/voucher/$',
        viewsets.VoucherGuideDeleteViewSet.as_view({'post': 'create'}),
        name='reportes_api-delete_guides'
    ),
    url(
        r'^api/voucher-guide-items/(?P<pk>[-\w]+)/$',
        viewsets.GuideItemsListViewSet.as_view({'get': 'list'}),
        name='reportes_api-list_items_guides'
    ),
    #url para lista de items buscados por fecha de guia
    url(
        r'^api/items-guide/(?P<date>[-\w]+)/$',
        viewsets.SearchDetailGuideViewSet.as_view({'get': 'list'}),
        name='reportes_api-items_guide_date'
    ),
]
