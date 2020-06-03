# -*- encoding: utf-8 -*-
from django.shortcuts import redirect
from django.views.generic.edit import FormView, UpdateView
from django.views.generic import View
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect

# Autentificacion de usuario
from django.contrib.auth import authenticate, login, logout

from django.views.generic import (
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
    ListView,
    TemplateView,
)

#app Caja
from applications.caja.models import Payment

#app adminnistracion
from applications.reportes.functions import facturas_sin_nota

from .models import User
from .forms import LoginForm

class HomeView(TemplateView):
    template_name = 'users/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['num_facturas'] = len(facturas_sin_nota())
        context['num_agentes'] = len(Payment.objects.seguimiento_agentes())
        return context


class LogIn(FormView):
    '''
    Logeo del usuario
    '''
    template_name = 'users/login.html'
    success_url = reverse_lazy('users_app:home')
    form_class = LoginForm

    def form_valid(self, form):
        print 'metodo post'
        # Verfiamos si el usuario y contrasenha son correctos.
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )

        if user is not None:
            if user.is_active and user.type_user == '1':
                login(self.request, user)
                return HttpResponseRedirect(
                    reverse(
                        'users_app:home'
                    )
                )

            else:
                return HttpResponseRedirect(
                    reverse(
                        'users_app:login'
                    )
                )


class LogoutView(View):
    """
    cerrar sesion
    """
    url = '/auth/login/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                'users_app:login'
            )
        )
