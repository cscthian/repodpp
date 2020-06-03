# -*- encoding: utf-8 -*-
from django.shortcuts import redirect
from datetime import datetime
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    TemplateView,
    ListView,
    DeleteView,
    CreateView,
    DetailView,
)

class LiquidacionDiariaView(TemplateView):
    template_name = 'caja/liquidacion/index.html'


class LiquidacionGuiaView(TemplateView):
    template_name = 'caja/liquidacion/liquidacion.html'


class MovimientosCajaView(TemplateView):
    template_name = 'caja/liquidacion/movimientos.html'


class LiquidacionProviderView(TemplateView):
    template_name = 'caja/liquidacion/liquidacion_provider.html'

class LiquidacionDiariaProvidorView(TemplateView):
    template_name = 'caja/liquidacion/liquidacion_dia.html'
