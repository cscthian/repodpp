# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic.edit import FormView

from applications.almacen.recepcion.models import Guide, DetailGuide

from .forms import DevolutionForm


class DevolutionView(FormView):
    form_class = DevolutionForm
    success_url = '.'
    template_name = 'almacen/devolucion/guide.html'

    def form_valid(self, form):
        #recuperamos los datos del forulario
        guides = form.cleaned_data['guide']
        for g in guides:
            #actualimaos las guias
            g.returned = True
            g.save()
            #actualimos las guias detalle
            detail_guides = DetailGuide.objects.filter(
                anulate=False,
                guide=g,
            )
            for dg in detail_guides:
                dg.returned = True
                dg.save()

        return super(DevolutionView, self).form_valid(form)
