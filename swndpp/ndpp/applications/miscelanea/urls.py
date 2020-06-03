from django.conf.urls import url, include
from . import views

urlpatterns = [

    #rest de aplicacion recepcion
    url(r'^', include('applications.miscelanea.url_services', namespace="miscelanea_servis_url")),
]
