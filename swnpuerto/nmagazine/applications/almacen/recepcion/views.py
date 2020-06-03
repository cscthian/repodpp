# -*- encoding: utf-8 -*-
from django.shortcuts import render
import operator
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.views.generic import (
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
    ListView,
    TemplateView,
    View,
)
from .models import (
    Magazine,
    MagazineDay,
    Guide,
    DetailGuide,
)
from .forms import (
    MagazineForm,
    MagazineUpdateForm,
    GuideForm,
    DetailGuideForm,
    ProductForm,
    ProductAddForm,
)

from applications.caja.pagos.models import Payment
# Create your views here.


class MagazineCreate(CreateView):
    """vista para crear un diario"""
    form_class = MagazineForm
    success_url = success_url = reverse_lazy('recepcion_app:magazine-list')
    template_name = 'almacen/recepcion/magazine/add.html'

    def form_valid(self, form):
        #guardamos magazine y recuperaos objeto
        magazine = form.save(commit=False)
        magazine.user_created = self.request.user

        magazine.tipo = '0'
        magazine.afecto = True
        magazine.save()

        for dia in ['0','1','2','3','4','5']:
            magazine_dia1 = MagazineDay(
                magazine=magazine,
                day=dia,
                precio_tapa=form.cleaned_data['precio_tapa'],
                precio_guia=form.cleaned_data['precio_guia'],
                precio_venta=form.cleaned_data['precio_venta'],
                user_created=self.request.user,
            )
            magazine_dia1.save()

        #registro de producto dia-domingo
        magazine_dia2 = MagazineDay(
            magazine=magazine,
            day='6',
            precio_tapa=form.cleaned_data['precio_tapad'],
            precio_guia=form.cleaned_data['precio_guiad'],
            precio_venta=form.cleaned_data['precio_ventad'],
            user_created=self.request.user,
        )
        magazine_dia2.save()

        return super(MagazineCreate, self).form_valid(form)


class ProductCreate(CreateView):
    """vista para crear un prodcuto"""
    form_class = ProductAddForm
    success_url = success_url = reverse_lazy('recepcion_app:magazine-list')
    template_name = 'almacen/recepcion/magazine/add_prod.html'

    def form_valid(self, form):
        #guardamos magazine y recuperaos objeto
        magazine = form.save(commit=False)
        magazine.user_created = self.request.user

        magazine.tipo = '1'
        magazine.save()

        #prducto
        sponsor = form.cleaned_data['sponsor']
        magazine.tipo = '1'
        if sponsor:
            magazine.sponsor = sponsor.pk
        magazine.save()

        #registro de produto lines-sabado
        magazine_dia1 = MagazineDay(
            magazine=magazine,
            day='7',
            precio_tapa=form.cleaned_data['precio_tapa'],
            precio_guia=form.cleaned_data['precio_guia'],
            precio_venta=form.cleaned_data['precio_venta'],
            user_created=self.request.user,
        )
        magazine_dia1.save()

        return super(ProductCreate, self).form_valid(form)


class DaysTemplateView(TemplateView):
    template_name = 'almacen/recepcion/magazine/days.html'

    def get_context_data(self, **kwargs):
        context = super(DaysTemplateView, self).get_context_data(**kwargs)
        lista_dias = {
            '0':'LUNES',
            '1':'MARTES',
            '2':'MIERCOLES',
            '3':'JUEVES',
            '4':'VIERNES',
            '5':'SABADO',
            '6':'DOMINGO',
        }
        days = sorted(lista_dias.items(), key=operator.itemgetter(0))
        context['days'] = days
        context['tipo'] = self.kwargs.get('tipo',0)
        context['pk'] = self.kwargs.get('pk',0)
        return context


class MagazineUpdateView(UpdateView):
    """vista para modificar un diario"""
    model = Magazine
    form_class = MagazineUpdateForm
    success_url = success_url = reverse_lazy('recepcion_app:magazine-list')
    template_name = 'almacen/recepcion/magazine/update.html'

    def get_initial(self, **kwargs):
        pk_dia = self.kwargs.get('day',0)
        day_ls = MagazineDay.objects.get(
            magazine=self.get_object(),
            day=pk_dia,
        )

        # recuperamos el objeto equipo
        initial = super(MagazineUpdateView, self).get_initial()
        initial['precio_tapa'] = day_ls.precio_tapa
        initial['precio_guia'] = day_ls.precio_guia
        initial['precio_venta'] = day_ls.precio_venta
        return initial

    def get_context_data(self, **kwargs):
        context = super(MagazineUpdateView, self).get_context_data(**kwargs)
        pk_dia = self.kwargs.get('day',0)
        context['day'] = pk_dia
        context['tipo'] = self.kwargs.get('tipo',0)
        return context

    def form_valid(self, form):
        #recuperamos los nuevos valores de formulario
        precio_tapa = form.cleaned_data['precio_tapa']
        precio_guia = form.cleaned_data['precio_guia']
        precio_venta = form.cleaned_data['precio_venta']

        #recuperamos DAY Lunes a Sabado
        pk_dia = self.kwargs.get('day',0)
        day = MagazineDay.objects.get(
            magazine=self.get_object(),
            day=pk_dia,
        )
        #guardamos los nuevos datos
        day.precio_tapa = precio_tapa
        day.precio_guia = precio_guia
        day.precio_venta = precio_venta
        day.user_modified = self.request.user
        day.save()
        return super(MagazineUpdateView, self).form_valid(form)


class ProductUpdateView(UpdateView):
    """vista para modificar un produco"""
    model = Magazine
    form_class = ProductAddForm
    success_url = success_url = reverse_lazy('recepcion_app:magazine-list')
    template_name = 'almacen/recepcion/magazine/add_prod.html'

    def get_initial(self):
        day_ls = MagazineDay.objects.get(
            magazine=self.get_object(),
            day='7',
        )

        # recuperamos datos del objeto Magazine_day
        initial = super(ProductUpdateView, self).get_initial()

        #vrificamos si tiene sponsor
        if self.get_object().sponsor:
            initial['sponsor'] = self.get_object().sponsor

        return initial

    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        context['tipo'] = self.kwargs.get('tipo',0)
        return context

    def form_valid(self, form):
        sponsor = form.cleaned_data['sponsor']
        magazine = form.save()
        if sponsor:
            magazine.sponsor = sponsor.pk
        #recuperamos los nuevos valores de formulario
        precio_tapa = form.cleaned_data['precio_tapa']
        precio_guia = form.cleaned_data['precio_guia']
        precio_venta = form.cleaned_data['precio_venta']

        #recuperamos DAY Lunes a Sabado
        day_ls = MagazineDay.objects.get(
            magazine=self.get_object(),
            day='7',
        )
        #guardamos los nuevos datos
        day_ls.precio_tapa = precio_tapa
        day_ls.precio_guia = precio_guia
        day_ls.precio_venta = precio_venta
        day_ls.user_modified = self.request.user
        day_ls.save()
        return super(ProductUpdateView, self).form_valid(form)


class ProductCreatePlantillaView(CreateView):
    """vista para crear un producto en base a una palantilla"""
    model = Magazine
    form_class = ProductAddForm
    success_url = success_url = reverse_lazy('recepcion_app:magazine-list')
    template_name = 'almacen/recepcion/magazine/plantilla.html'

    def get_initial(self):
        pk_magazine = self.kwargs.get('pk',0)
        magazine = Magazine.objects.get(pk=pk_magazine)
        # recuperamos datos del objeto Magazine_day
        initial = super(ProductCreatePlantillaView, self).get_initial()

        #vrificamos si tiene sponsor
        if magazine.sponsor:
            initial['sponsor'] = self.get_object().sponsor

        initial['name'] = magazine.name
        initial['provider'] = magazine.provider
        initial['description'] = magazine.description
        initial['day_expiration'] = magazine.day_expiration
        initial['code'] = magazine.code
        initial['afecto'] = magazine.afecto

        return initial

    def get_context_data(self, **kwargs):
        context = super(ProductCreatePlantillaView, self).get_context_data(**kwargs)
        context['tipo'] = self.kwargs.get('tipo',0)
        pk_magazine = self.kwargs.get('pk',0)
        context['object'] = Magazine.objects.get(pk=pk_magazine)
        return context

    def form_valid(self, form):
        #creamos objeto magazine
        magazine = form.save(commit=False)
        magazine.user_created = self.request.user

        magazine.tipo = '1'
        magazine.save()
        sponsor=form.cleaned_data['sponsor']
        if sponsor:
            magazine.sponsor = sponsor.pk

        magazine.save()

        #registro de produto lines-sabado
        magazine_dia1 = MagazineDay(
            magazine=magazine,
            day='7',
            precio_tapa=form.cleaned_data['precio_tapa'],
            precio_guia=form.cleaned_data['precio_guia'],
            precio_venta=form.cleaned_data['precio_venta'],
            user_created=self.request.user,
        )
        magazine_dia1.save()
        return super(ProductCreatePlantillaView, self).form_valid(form)


class MagazineDeleteView(DeleteView):
    """vista para anular un diario o producto"""
    model = Magazine
    success_url = success_url = reverse_lazy('recepcion_app:magazine-list')
    template_name = 'almacen/recepcion/magazine/delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.disable = True
        self.object.user_modified = self.request.user
        self.object.save()
        success_url = self.get_success_url()

        return HttpResponseRedirect(success_url)


class MagazineListView(TemplateView):
    """vista para listar producto o diario"""
    template_name = 'almacen/recepcion/magazine/list.html'


class GuideRegisterView(TemplateView):
    """vista para registrar guias"""
    template_name = 'almacen/recepcion/guide/add.html'


class GuideListView(TemplateView):
    """vista para lista de consulta de guias"""
    template_name = 'almacen/recepcion/guide/list.html'


class GuideUpdateView(UpdateView):
    """vista para modificar datos claves de una guia"""
    model = Guide
    form_class = GuideForm
    success_url = reverse_lazy('recepcion_app:guide-list')
    template_name = 'almacen/recepcion/guide/update.html'

    def get_context_data(self, **kwargs):
        context = super(GuideUpdateView, self).get_context_data(**kwargs)
        guide = self.get_object()
        context['list_detail'] = DetailGuide.objects.filter(
            guide=guide,
            anulate=False,
        )
        context['pagos'] = Payment.objects.filter(
            anulate=False,
            detail_asignation__asignation__detail_guide__guide__pk=guide.pk,
        ).count()
        return context

    def form_valid(self, form):
        guide = self.get_object()
        guide.user_modified = self.request.user
        guide.save()
        return super(GuideUpdateView, self).form_valid(form)


class GuideDetailView(DetailView):
    model = Guide
    template_name = 'almacen/recepcion/guide/detail.html'

    def get_context_data(self, **kwargs):
        context = super(GuideDetailView, self).get_context_data(**kwargs)
        guide = self.get_object()
        context['list_detail'] = DetailGuide.objects.filter(
            guide=guide,
            anulate=False,
        )
        return context



class GuideDeleteView(DeleteView):
    model = Guide
    success_url = reverse_lazy('recepcion_app:guide-list')
    template_name = 'almacen/recepcion/guide/delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.anulate = True
        self.object.user_modified = self.request.user
        self.object.save()
        success_url = self.get_success_url()

        return HttpResponseRedirect(success_url)


class DetailGuideUpdateView(UpdateView):
    model = DetailGuide
    form_class = DetailGuideForm
    template_name = 'almacen/recepcion/guide/detail_update.html'

    def form_valid(self, form):
        form.save()
        detail_guide = self.get_object()
        guide = detail_guide.guide

        guide.user_modified = self.request.user
        detail_guide.user_modified = self.request.user
        guide.save()
        detail_guide.save()

        return HttpResponseRedirect(
            reverse(
                'recepcion_app:guide-update',
                kwargs={'pk': guide.pk },
            )
        )


class DetailGuideDeleteView(DeleteView):
    model = DetailGuide
    success_url = reverse_lazy('recepcion_app:guide_list')
    template_name = 'almacen/recepcion/guide/detail_delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        guide = self.object.guide

        self.object.anulate = True
        self.object.user_modified = self.request.user
        guide.user_modified = self.request.user

        self.object.save()
        guide.save()

        return HttpResponseRedirect(
            reverse(
                'recepcion_app:guide-update',
                kwargs={'pk': guide.pk },
            )
        )


class ProducAddView(TemplateView):
    template_name = 'almacen/recepcion/magazine/add_prod.html'


class ProducPorCobrarView(TemplateView):
    """vista que lista productos que se cobraran en un fecha"""
    template_name = 'almacen/recepcion/consultas/prod_por_cobrar.html'
