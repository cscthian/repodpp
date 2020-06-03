from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.contrib import admin
#import debug_toolbar

urlpatterns = [
    #urls para usuario
    url(r'^', include('applications.users.urls', namespace="users_app")),
    url(r'^', include('applications.miscelanea.urls', namespace="miscelanea_app")),
    url(r'^', include('applications.recepcion.urls', namespace="recepcion_app")),
    url(r'^', include('applications.caja.urls', namespace="caja_app")),
    url(r'^', include('applications.reportes.urls', namespace="reportes_app")),
    url(r'^', include('applications.administracion.urls', namespace="administracion_app")),

    url(r'^admin/', admin.site.urls),
]
