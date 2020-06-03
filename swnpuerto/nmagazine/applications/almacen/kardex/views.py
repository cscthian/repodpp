from django.shortcuts import render
from django.views.generic import (
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
    ListView,
    TemplateView,
    View,
)

from applications.almacen.recepcion.models import MagazineDay

# Create your views here.
class KardexTemplateView(TemplateView):
    template_name = 'almacen/kardex/inventario.html'


class ConstatarView(TemplateView):
    template_name = 'almacen/kardex/constatar.html'


class DetalleInventarioView(DetailView):
    model = MagazineDay
    template_name = 'almacen/kardex/detalle.html'


class MagazineEnAlmacenView(TemplateView):
    """vista que lista Reporte de Prouctos en Almacen"""
    template_name = 'almacen/kardex/en_almacen.html'
