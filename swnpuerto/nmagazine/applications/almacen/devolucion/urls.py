# -*- encoding: utf-8 -*-
from django.conf.urls import url, include
from . import views

urlpatterns = [
    #url para devolucion
    url(
        r'^almacen/devolver/guias/$',
        views.DevolutionView.as_view(),
        name='devolver-guias'
    ),
]
