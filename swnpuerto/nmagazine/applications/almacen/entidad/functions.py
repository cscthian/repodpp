from datetime import datetime
from applications.almacen.recepcion.models import Guide, DetailGuide


#corremos scrip para actualizar ultimos scrip
def execute_scrip(rango):
    ran = int(rango)
    guides = DetailGuide.objects.filter(
        anulate=False,
    )[:ran]
    #
    for g in guides:
        g.created = datetime.now()
        g.save()

    return 'Rescrito correctamente'
