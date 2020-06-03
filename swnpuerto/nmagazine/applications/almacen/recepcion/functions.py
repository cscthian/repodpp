# -*- encoding: utf-8 -*-
from applications.almacen.recepcion.models import DetailGuide, Guide


#creamos calse que rpresenta una pauta

class GuideDetail():
      day = ''
      count = 0
      guide = ''


def guide_detail(pk_dg):
    #recuperamos la guia
    guide = Guide.objects.get(pk=pk_dg)
    list_guides = DetailGuide.objects.filter(
        guide=guide,
        anulate=False,
    )
    #lista resultado
    resultado = []

    for dg in list_guides:
        guia = GuideDetail()
        guia.day = dg.magazine_day.pk
        guia.count = dg.count
        #agegamos a la lista
        resultado.append(guia)

    return resultado
