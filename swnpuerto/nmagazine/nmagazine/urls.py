from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.contrib import admin
#import debug_toolbar

urlpatterns = [
    url(r'^', include('applications.users.urls', namespace="users_app")),
    url(r'^', include('applications.almacen.entidad.urls', namespace="entidad_app")),
    url(r'^', include('applications.almacen.recepcion.urls', namespace="recepcion_app")),
    url(r'^', include('applications.almacen.kardex.urls', namespace="kardex_app")),
    url(r'^', include('applications.almacen.asignacion.urls', namespace="asignacion_app")),
    url(r'^', include('applications.almacen.devolucion.urls', namespace="devolucion_app")),
    url(r'^', include('applications.caja.pagos.urls', namespace="pagos_app")),
    url(r'^', include('applications.caja.liquidacion.urls', namespace="liquidacion_app")),
    url(r'^', include('applications.reportes.urls', namespace="reportes_app")),
    url(r'^', include('applications.administrador.urls', namespace="administrador_app")),
    url(r'^', include('applications.control.urls', namespace="control_app")),

    url(r'^admin/', admin.site.urls),
    #url(r'^__debug__/', include(debug_toolbar.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
