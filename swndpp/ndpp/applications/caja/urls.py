from django.conf.urls import url, include
from . import views

urlpatterns = [
    #url para registrar Pagos
    url(
        r'^registrar-pagos/$',
        views.PaymentRegister.as_view(),
        name='add-payment'
    ),

    #url para anular pago agente
    url(
        r'^caja/cobros/cobrar/anular/(?P<pk>\d+)/$',
        views.PaymentDeleteView.as_view(),
        name='pagos-anular'
    ),
    #url para liquidacion diaria
    url(
        r'^caja/liquidacion/diaria/$',
        views.LiquidacionDiariaView.as_view(),
        name='liquidacion_dia-payment'
    ),


    #rest de aplicacion recepcion
    url(r'^', include('applications.caja.url_services', namespace="caja_servis_url")),
]
