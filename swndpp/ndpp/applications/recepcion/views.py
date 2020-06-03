# -*- encoding: utf-8 -*-
from django.shortcuts import render
import operator
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

from applications.reportes.forms import SearchGuideForm
from .models import (
    Magazine,
    MagazineDay,
    Guide,
    DetailGuide,
)

from .forms import (
    MagazineForm,
    ProductAddForm,
    MagazineUpdateForm,
)


class MagazineListView(TemplateView):
    """vista para listar producto o diario"""
    template_name = 'recepcion/magazine/list.html'


class MagazineCreate(CreateView):
    """vista para crear un diario"""
    form_class = MagazineForm
    success_url = reverse_lazy('recepcion_app:list-magazine')
    template_name = 'recepcion/magazine/add.html'

    def form_valid(self, form):
        print '****************'
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
    success_url = reverse_lazy('recepcion_app:list-magazine')
    template_name = 'recepcion/magazine/add_prod.html'

    def form_valid(self, form):
        #guardamos magazine y recuperaos objeto
        magazine = form.save(commit=False)
        magazine.user_created = self.request.user

        magazine.tipo = '1'
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
    template_name = 'recepcion/magazine/days.html'

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
    success_url = success_url = reverse_lazy('recepcion_app:list-magazine')
    template_name = 'recepcion/magazine/update.html'

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
        dias = ['LUNES','MARTES','MIERCOLES','JUEVES','VIERNES','SABADO','DOMINGO']
        context['day'] = dias[int(pk_dia)]
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
    success_url = success_url = reverse_lazy('recepcion_app:list-magazine')
    template_name = 'recepcion/magazine/add_prod.html'

    def get_initial(self):
        day_ls = MagazineDay.objects.get(
            magazine=self.get_object(),
            day='7',
        )

        # recuperamos datos del objeto Magazine_day
        initial = super(ProductUpdateView, self).get_initial()

        return initial

    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        context['tipo'] = self.kwargs.get('tipo',0)
        return context

    def form_valid(self, form):
        magazine = form.save()
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
    success_url = success_url = reverse_lazy('recepcion_app:list-magazine')
    template_name = 'recepcion/magazine/plantilla.html'

    def get_initial(self):
        pk_magazine = self.kwargs.get('pk',0)
        magazine = Magazine.objects.get(pk=pk_magazine)
        # recuperamos datos del objeto Magazine_day
        initial = super(ProductCreatePlantillaView, self).get_initial()

        initial['name'] = magazine.name
        initial['provider'] = magazine.provider
        initial['description'] = magazine.description
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
    success_url = reverse_lazy('recepcion_app:list-magazine')
    template_name = 'recepcion/magazine/delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.disable = True
        self.object.user_modified = self.request.user
        self.object.save()
        success_url = self.get_success_url()

        return HttpResponseRedirect(success_url)


class GuideRegisterView(TemplateView):
    """vista para registrar guias"""
    template_name = 'recepcion/guide/add.html'



class SearchGuideView(ListView):
    '''
        busqueda de guias
    '''
    context_object_name = 'guias'
    template_name = 'recepcion/guide/list.html'

    def get_context_data(self, **kwargs):
        context = super(SearchGuideView, self).get_context_data(**kwargs)
        context['form'] = SearchGuideForm
        return context

    def get_queryset(self):
        q = self.request.GET.get("item", '')
        r = self.request.GET.get("date", '')

        print '****************'
        print q
        print r
        #recuperamos guias
        if (r != ''):
            print 'se ingreso la fecha'
            queryset = Guide.objects.filter(
                anulate=False,
                number__icontains=q,
                created__gte=r,
            )
        else:
            print 'no se ingreso la fecha'
            print r
            queryset = DetailGuide.objects.filter(
                anulate=False,
                number__icontains=q,
            )[:20]

        return queryset
