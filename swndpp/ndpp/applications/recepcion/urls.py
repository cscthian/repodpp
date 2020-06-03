from django.conf.urls import url, include
from . import views

urlpatterns = [
    #url para home de la aplicacion
    url(
        r'^guia-registrar/$',
        views.GuideRegisterView.as_view(),
        name='add-guide'
    ),
    #url para listar guias
    url(
        r'^guia-lista/$',
        views.SearchGuideView.as_view(),
        name='list-guide'
    ),
    #url para listar diarios
    url(
        r'^magazine-listar/$',
        views.MagazineListView.as_view(),
        name='list-magazine'
    ),
    #url para agregar diarios
    url(
        r'^magazine-add/$',
        views.MagazineCreate.as_view(),
        name='add-magazine'
    ),
    #url para agregar productos
    url(
        r'^prod-add/$',
        views.ProductCreate.as_view(),
        name='add-prod'
    ),
    #url para listar diarios
    url(
        r'^lista-dias-diarios/(?P<pk>\d+)/(?P<tipo>\d+)/$',
        views.DaysTemplateView.as_view(),
        name='list_day-magazine'
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




    #rest de aplicacion recepcion
    url(r'^', include('applications.recepcion.url_services', namespace="recepcion_servis_url")),
]
