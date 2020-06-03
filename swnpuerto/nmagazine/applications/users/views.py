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

from .models import User
from .forms import LoginForm, UserForm, UserUpdateForm


class LogIn(FormView):
    '''
    Logeo del usuario
    '''
    template_name = 'users/login/login.html'
    success_url = reverse_lazy('users_app:home-almacen')
    form_class = LoginForm

    def form_valid(self, form):
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
                        'users_app:home-almacen'
                    )
                )

            elif user.is_active and user.type_user == '2':
                login(self.request, user)
                return HttpResponseRedirect(
                    reverse(
                        'users_app:home-caja'
                    )
                )

            elif user.is_active and user.type_user == '3':
                login(self.request, user)
                return HttpResponseRedirect(
                    reverse(
                        'users_app:home-almacen'
                    )
                )

            elif user.is_active and user.type_user == '4':
                login(self.request, user)
                return HttpResponseRedirect(
                    reverse(
                        'administrador_app:home-admin'
                    )
                )

            elif user.is_active:
                # si el usuario es activo ira dahboard
                login(self.request, user)
                return super(LogIn, self).form_valid(form)
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


#mantenimietos para usuarios
class UserListView(LoginRequiredMixin, ListView):
    '''
    metodo para listar usuarios
    '''
    context_object_name = 'users_list'
    model = User
    login_url = reverse_lazy('users_app:login')
    template_name = 'users/usuarios/list.html'

    def get_queryset(self):
        queryset = User.objects.filter(
            is_superuser=False,
            is_active=True,
        )
        return queryset


class UserCreateView(LoginRequiredMixin, FormView):
    '''
        vista para registrar usuarios
    '''
    model = User
    form_class = UserForm
    login_url = reverse_lazy('users_app:login')
    success_url = reverse_lazy('users_app:user-list')
    template_name = 'users/usuarios/add.html'

    def form_valid(self, form):
        #registramos usuario
        usuario = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            type_user=form.cleaned_data['type_user'],
        )
        usuario.save()

        return super(UserCreateView, self).form_valid(form)
#
#
class UserUpdateView(LoginRequiredMixin, UpdateView):
    '''
        vista para modificar un usuario
    '''
    model = User
    template_name = 'users/usuarios/update.html'
    form_class = UserUpdateForm
    login_url = reverse_lazy('users_app:login')
    success_url = reverse_lazy('users_app:user-list')


class UserDeleteView(LoginRequiredMixin, DeleteView):
    '''
        vista para eliminar un usuario
    '''
    model = User
    login_url = reverse_lazy('users_app:login')
    success_url = reverse_lazy('users_app:user-list')
    template_name = 'users/usuarios/delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        usuario = self.object
        #Desactivamos usuario
        usuario.is_active = False
        usuario.is_staff = False
        usuario.save()
        success_url = self.get_success_url()

        return HttpResponseRedirect(success_url)


class AlmacenTemplateView(TemplateView):
    template_name = 'almacen/panel.html'


class CajaTemplateView(TemplateView):
    template_name = 'caja/panel.html'
