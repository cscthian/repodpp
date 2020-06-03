from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^$',
        views.LogIn.as_view(),
        name='login'
    ),
    url(
        r'^salir/$',
        views.LogoutView.as_view(),
        name='logout'
    ),
    url(
        r'^panel/$',
        views.AlmacenTemplateView.as_view(),
        name='home-almacen'
    ),
    url(
        r'^panel/caja/$',
        views.CajaTemplateView.as_view(),
        name='home-caja'
    ),
    #urls para crear usuarios
    url(
        r'^admin/usuarios/panel/lista$',
        views.UserListView.as_view(),
        name='user-list'
    ),
    url(
        r'^admin/usuarios/panel/add$',
        views.UserCreateView.as_view(),
        name='user-add'
    ),
    url(
        r'^admin/usuarios/panel/update/(?P<pk>\d+)/$',
        views.UserUpdateView.as_view(),
        name='user-update'
    ),
    url(
        r'^admin/usuarios/panel/delete/(?P<pk>\d+)/$',
        views.UserDeleteView.as_view(),
        name='user-delete'
    ),
]
