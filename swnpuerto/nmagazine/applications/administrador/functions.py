from datetime import datetime, timedelta

from applications.almacen.entidad.models import Vendor
from applications.almacen.recepcion.models import Guide, DetailGuide
from applications.almacen.asignacion.models import Asignation, DetailAsignation
from applications.caja.pagos.functions import (
    por_cobrar,
    devolucion_movimientos,
    tope_canilla
)
from applications.caja.pagos.models import Payment, Invoce, Venta
from .models import Boleta, DetailBoleta

#calse que representa un resumen del dia
class Resumen():
    ventas_dia = 0
    deuda = 0
    devuelto = 0
    magazine_registrado = 0
    magazine_asignado = 0
    guias_anuladas = 0
    canillas_tope = 0
    boletas_anuladas = 0
    faltantes = 0

#calse que representa una venta dia
class VentaDia():
    label = ''
    value = 0


class NotaItem():
    pk = ''
    name = ''
    precio_guia = 0
    precio_venta = 0
    count = 0
    date = ''


class ItemBoleta():
    pk = ''
    codigo = ''
    total = 0
    magazine = ''
    vendor = ''
    number = ''
    client = ''
    date_emition = ''
    date_venta = ''
    count = 0
    precio_venta = 0
    precio_sunat = 0
    amount = 0
    afecto = True
    addressee = ''
    emitido = True
    impreso = False


def calcular_resumen():
    fecha = datetime.now()
    #creamos objeto resumen
    r = Resumen()
    ventas_returned = Payment.objects.ventas_returned_dia(fecha)
    #verificamos si la suma exise
    if ventas_returned['amount__sum'] == None:
        ventas_returned['amount__sum'] = 0
    #
    if ventas_returned['count_return__sum'] == None:
        ventas_returned['count_return__sum'] = 0
    #
    r.ventas_dia = ventas_returned['amount__sum'] + Venta.objects.ventas_dia(fecha)
    r.devuelto = ventas_returned['count_return__sum']
    r.magazine_registrado = DetailGuide.objects.magazine_count_register(fecha)
    r.magazine_asignado = DetailAsignation.objects.count_asignation_day(fecha)
    r.guias_anuladas = len(Guide.objects.filter(anulate=True,created__date=fecha))
    #calculamos faltantes
    vendors = Vendor.objects.filter(
        anulate = False,
    )
    r.faltantes = len(Payment.objects.vendor_faltantes(vendors))
    r.boletas_anuladas = len(Invoce.objects.filter(anulate=True,created__date=fecha))

    r.canillas_tope = 0
    return r


#funcion que devuleve las ultimas 7 ventas dia
def ultimas_ventas():
    fechas = [
        datetime.now() - timedelta(days=6),
        datetime.now() - timedelta(days=5),
        datetime.now() - timedelta(days=4),
        datetime.now() - timedelta(days=3),
        datetime.now() - timedelta(days=2),
        datetime.now() - timedelta(days=1),
        datetime.now(),
    ]
    #creamos arreglo resultado
    resultado = []
    dias = [
        'Lunes',
        'Martes',
        'Miercoles',
        'Jueves',
        'Viernes',
        'Sabado',
        'Domingo',
    ]
    for fecha in fechas:
        v = VentaDia()
        v.label = str(fecha.day) + ' - '+dias[fecha.weekday()]
        v.value = Payment.objects.ventas_returned_dia(fecha)['amount__sum']
        resultado.append(v)

    return resultado


#funcion que devuelve la lista de itemas de una guia
def guide_items(guide):
    details = DetailGuide.objects.filter(
        anulate=False,
        guide__number=guide,
    )
    resultado = []
    for d in details:
        nota_item = NotaItem()
        nota_item.pk = d.pk
        days = [
            'lunes',
            'martes',
            'miercoles',
            'jueves',
            'viernes',
            'sabado',
            'domingo'
        ]
        aux = d.magazine_day.day
        nota_item.name = str(d.magazine_day.magazine.name) +'--'+ str(days[int(aux)])
        nota_item.precio_guia = d.precio_guia
        nota_item.precio_venta = d.precio_unitario
        nota_item.count = d.count
        nota_item.date = d.guide.date
        resultado.append(nota_item)

    return resultado


def verificar_estado_impreso(magazine_day, date, date2):
    #funcion que devuelve el estado impreo de un magazine day
    if date2 == date:
        return DetailBoleta.objects.existe_magazine(magazine_day,date)
    else:
        return DetailBoleta.objects.existe_magazine2(magazine_day,date,date2)



def items_boleta(fecha,fecha2):
    #arrelgo de dias
    dias = [
        'LUN',
        'MAR',
        'MIE',
        'JUE',
        'VIE',
        'SAB',
        'DOM',
        ' '
    ]
    #convertimos la fecha
    date = datetime.strptime(fecha, '%d-%m-%Y').date()
    date2 = datetime.strptime(fecha, '%d-%m-%Y').date()
    if fecha2 == fecha:
        consulta = Payment.objects.magazine_boleta(date)
    else:
        date2 = datetime.strptime(fecha2, '%d-%m-%Y').date()
        consulta = Payment.objects.magazine_boleta2(date,date2)

    resultado = []
    for c in consulta:
        print '======='
        print c
        if c['count'] > 0:
            itemboleta = ItemBoleta()
            a = str(c['detail_asignation__asignation__detail_guide__guide__date'].year)
            m = str(c['detail_asignation__asignation__detail_guide__guide__date'].month)
            d = str(c['detail_asignation__asignation__detail_guide__guide__date'].day)
            # a = str(c['detail_asignation__asignation__created'].year)
            # m = str(c['detail_asignation__asignation__created'].month)
            # d = str(c['detail_asignation__asignation__created'].day)
            itemboleta.magazine = c['magazine'] +' '+ dias[int(c['dia'])]+"    "+d+"/"+m+"/"+a
            #
            # if c['vendor_type'] == '1':
            #     itemboleta.vendor = c['vendor']
            # else:
            #     itemboleta.vendor = '00000'
            #
            itemboleta.codigo = 'C00'+str(c['detail_asignation__asignation__detail_guide'])
            itemboleta.pk = c['detail_asignation__asignation__detail_guide']
            itemboleta.guide = c['guide']
            itemboleta.date_venta = c['detail_asignation__asignation__detail_guide__guide__date']
            itemboleta.count = c['count']
            itemboleta.precio_venta = c['detail_asignation__asignation__detail_guide__precio_unitario']
            itemboleta.precio_sunat = c['detail_asignation__asignation__detail_guide__precio_unitario']
            itemboleta.amount = c['amount']
            itemboleta.afecto = c['detail_asignation__asignation__detail_guide__magazine_day__magazine__afecto']
            itemboleta.addressee = c['addressee']
            #
            #verificamos si el item ya se imprimio
            detail_guide = DetailGuide.objects.get(
                pk=c['detail_asignation__asignation__detail_guide']
            )
            itemboleta.impreso = verificar_estado_impreso(
                detail_guide.magazine_day,
                date,
                date2,
            )
            #
            if itemboleta.impreso == True:
                itemboleta.emitido = False

            resultado.append(itemboleta)

    return resultado


#scrip para cambiar las guias de destinatario
def cambiar_destinatario_guias():
    guias = Guide.objects.filter(
        anulate=False,
    )
    for g in guias:
        if g.provider.name == 'CIA DISTRIBUIDORA NACIONAL DE REVISTAS S.A.C.':
            g.addressee = '0'
            g.save()
            print 'Guia actualizada a dpp'
        # else:
        #     g.addressee = '1'
        #     g.save()
        #     print 'guia actualizada a MAx'

    return True
