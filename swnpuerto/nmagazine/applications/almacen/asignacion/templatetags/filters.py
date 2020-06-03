from django import template


register = template.Library()


@register.filter(name='split_label_devolution')
#sepra un texto por el caracter *
def split_label_devolution(value):
    arreglo = value.split('*')
    return arreglo

@register.filter(name='identificar_dia')
def identificar_dia(value):
    print '===='
    print value
    if value == '0':
        return 'LUNES'
    elif value == '1':
        return 'MARTES'
    elif value == '2':
        return 'MIERCOLES'
    elif value == '3':
        return 'JUEVES'
    elif value == '4':
        return 'VIERNES'
    elif value == '5':
        return 'SABADO'
    elif value == '6':
        return 'DOMINGO'
    else:
        return 'LUNES-SABADO'
