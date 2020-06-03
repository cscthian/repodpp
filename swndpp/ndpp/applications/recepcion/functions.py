# aplicacion recepcion
from .models import DetailGuide

def items_by_guide(number):
    """  funcion que devuelve los items de un numero de guia """
    #declaramos diccionario de dias
    DAY_CHOICES = {
        '0':'LUNES',
        '1':'MARTES',
        '2':'MIERCOLES',
        '3':'JUEVES',
        '4':'VIERNES',
        '5':'SABADO',
        '6':'DOMINGO',
        '7':'LUNES-SABADO',
    }
    #recuperamos la consulta por numero de guia
    consulta = DetailGuide.objects.items_by_guide(number)
    #actualizamos el estado de dia
    for c in consulta:
        c['dia'] = DAY_CHOICES[c['dia']]

    #devolvemos valores actualizados
    return consulta
