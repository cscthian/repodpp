from django.conf.urls import url
from . import views, viewsets

urlpatterns = [
    #urls para servicios
    url(
        r'^api/save/voucher/$',
        viewsets.AddVoucherViewSet.as_view({'post': 'create'}),
        name='voucher-add'
    ),
    url(
        r'^api/voucher/recuperar/(?P<date>[-\w]+)/$',
        viewsets.RecuperarVoucherViewSet.as_view({'get': 'list'}),
        name='voucher-recuperar',
    ),
    #urls para serviios
    url(
        r'^control/guias/voucher_guides/(?P<guide>\d+)/$',
        views.VoucherGuideListView.as_view(),
        name='voucher-guides'
    ),
]
