# -*- encoding: utf-8 -*-
from datetime import datetime, timedelta
import operator

from applications.almacen.recepcion.models import MagazineDay, Guide, DetailGuide
from applications.almacen.entidad.models import Vendor
from applications.almacen.asignacion.models import DetailAsignation
from applications.caja.pagos.models import Payment, Venta

from .models import CierreMes


#objeto que representa un diario
class Ranking():
    pk = ''
    name = ''
    vendido = 0
    devuelto = 0
    perdido = 0
    monto = 0

#objeto que representa un ranking canilla
class RankingVendor():
    pk = ''
    cod = ''
    name = ''
    tipo = ''
    tope = 0
    deuda = 0
    entregado = 0
    vendido = 0
    devuelto = 0


#objeto que representa una Puntuacion
class Puntuacion():
    pk = ''
    cod = ''
    name = ''
    tipo = ''
    puntaje = []
    meses = []


#objeto que representa un canilla Cero
class CanillaCero():
    pk = ''
    cod = ''
    name = ''
    tipo = ''
    lunes = 0
    martes = 0
    miercoles = 0
    jueves = 0
    viernes = 0
    sabado = 0
    domingo = 0


class HistoryGuideResumen():
    total_vendido = 0
    total_deuda = 0
    total_almacen = 0
    count_vendido = 0
    count_deuda = 0
    count_almacen = 0
    count_real = 0


class HistoryGuide():
    date = ''
    count_dev = 0
    count_ven = 0
    count_tie = 0


class HistoryG():
    pk = ''
    magazine = ''
    precio_venta = 0
    count_reception = 0
    count_deliver = 0
    #
    total_vendido = 0
    total_deuda = 0
    total_almacen = 0
    count_vendido = 0
    count_deuda = 0
    count_almacen = 0
    count_devuelto = 0
    count_real = 0
    historia = []

class ResumenDetalleGuia():
    magazine = ''
    count_reception = 0
    count_deliver = 0
    count_diferencia = 0
    precio_venta = 0
    total_vendido = 0
    total_deuda = 0
    total_almacen = 0
    count_vendido = 0
    count_devuelto = 0
    count_deuda = 0
    count_almacen = 0
    count_real = 0
    count_perdida = 0
    amount_perdida = 0


class ResumenGuia():
    number = ''
    provider = ''
    date = ''
    amount_perdida = 0
    culmined = ''
    #
    itmes = []


def rankin_magazine(date1, date2, tipo):
    fecha1 = datetime.strptime(date1, '%d-%m-%Y').date()
    fecha2 = datetime.strptime(date2, '%d-%m-%Y').date()

    #recuperamos la lista de asignaciones detalle segun fechas
    if tipo == '0001':
        diarios = MagazineDay.objects.filter(
            magazine__disable=False,
        )
    else:
        diarios = MagazineDay.objects.filter(
            magazine__disable=False,
            magazine__tipo=tipo,
        )
    #consultamos movimientos para cada diaro en rango de fechas
    movimientos = Payment.objects.payment_by_date(fecha1,fecha2)
    #detalle guias

    #reamos arreglo resultado
    resultado = []
    for  d in diarios:
        rk = Ranking()
        rk.pk = d.pk
        rk.name = d
        rk.vendido = 0
        rk.devuelto = 0
        rk.perdido = 0
        rk.monto = 0
        #iteramos pagos
        for m in movimientos:
            aux_guias = []
            if m.detail_asignation.asignation.detail_guide.magazine_day==d:
                rk.vendido = rk.vendido + m.count_payment
                rk.devuelto = rk.devuelto + m.count_return
                #agregamos las guias aux_guias
                aux = m.detail_asignation.asignation.detail_guide
                if not aux in aux_guias:
                    rk.perdido = rk.perdido + aux.missing

                aux_guias.append(m.detail_asignation.asignation.detail_guide)

        #agregamos los resultados
        rk.monto = rk.perdido*d.precio_venta
        resultado.append(rk)

    resultado.sort(key = operator.attrgetter('vendido'), reverse=True)

    return resultado


#funcion que devleve lista de rankin canilla
def rankin_vendor(start_date, end_date, pk_magazine):
    #recuperamos todo los canillas
    canillas = Vendor.objects.filter(
        disable=False,
        type_vendor='0',
    )
    #creamos fecha por defeco
    #iteramos los canillas y recuperamos la asiganciones
    resultado = []
    for c in canillas:
        asignaciones = DetailAsignation.objects.asignation_by_fecha_vendor(
            start_date,
            end_date
        ).filter(
            vendor=c,
            asignation__detail_guide__magazine_day__magazine__pk=pk_magazine
        )
        rv = RankingVendor()
        rv.pk = c.pk
        rv.cod = c.cod
        rv.name = c.name
        rv.tipo = c.get_type_vendor_display
        rv.tope = c.line_credit
        rv.entregado = 0
        rv.devuelto = 0
        rv.deuda = 0
        rv.vendido = 0
        pagado = 0
        total = 0
        for a in asignaciones:
            rv.entregado = rv.entregado + a.count
            total = total + a.count*a.precio_venta
            rv.devuelto = rv.devuelto + Payment.objects.suma_return(a.pk)
            rv.vendido = rv.vendido  + Payment.objects.suma_payment(a.pk)
            pagado = pagado + (Payment.objects.suma_payment(a.pk)*a.precio_venta)
        #calculamos deuda
        rv.deuda = total - pagado
        #calculamos puntuacion
        resultado.append(rv)
        #ordenamos
        resultado.sort(key = operator.attrgetter('vendido'), reverse=True)

    return resultado


#funcion que devuelve el historial de canllas
def vendor_hisotorial():
    #recuperamos ultimos cierres de mes
    ultimos_cierre = CierreMes.objects.all().order_by('-date_start')[:3]
    #recuperamos lista de canillas
    canillas = Vendor.objects.filter(disable=False)
    #creamos el arreglo resultado
    resultado = []
    #filtramos ranking por cada mes
    for c in canillas:
        p = Puntuacion()
        p.pk = c.pk
        p.cod = c.cod
        p.name = c.name
        p.tipo = c.get_type_vendor_display
        p.meses = []
        p.puntaje = []
        #recuperamos asignaciones
        for cierre in ultimos_cierre:
            p.meses.append(cierre.mes)
            asig = DetailAsignation.objects.asignation_by_fecha_vendor(
                cierre.date_start,
                cierre.date_end,
            ).filter(vendor=c)
            devuelto = 0
            entregado = 0
            for a in asig:
                entregado = entregado + a.count
                devuelto = devuelto + Payment.objects.suma_return(a.pk)

            #calculamos e puntaje
            if entregado > 0:
                puntuacion = (devuelto*100)/entregado
                p.puntaje.append(str(puntuacion)+'%')
            else:
                p.puntaje.append('-')
        #agregamos resultado
        resultado.append(p)
    #procesamos resultado
    return resultado



#funcion que genera canillacero para cada canilla
def canilla_cero(pk_magazine):
    #recuperamos la fechas
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    #recuperamos los canilla
    canillas = Vendor.objects.filter(disable=False)
    #variable resultado
    resultado = []
    #recuperaos las asiganciones en el rango de fechass para cada canilla
    for c in canillas:
        canillacero = CanillaCero()
        canillacero.pk = c.pk
        canillacero.cod = c.cod
        canillacero.name = c.name
        canillacero.tipo = c.get_type_vendor_display
        canillacero.lunes = 0
        canillacero.martes = 0
        canillacero.miercoles = 0
        canillacero.jueves = 0
        canillacero.viernes = 0
        canillacero.sabado = 0
        canillacero.domingo = 0
        asignaciones = DetailAsignation.objects.asignation_by_fecha_vendor(
            start_date,
            end_date
        ).filter(
            vendor=c,
            asignation__detail_guide__magazine_day__magazine__pk=pk_magazine,
        )
        #calculamos sus devoluciones
        for a in asignaciones:
            canillacero.lunes =+ Payment.objects.suma_return(a.pk)
            if a.asignation.detail_guide.magazine_day.day == '0':
                canillacero.lunes =+ Payment.objects.suma_return(a.pk)
            elif a.asignation.detail_guide.magazine_day.day == '1':
                canillacero.martes =+ Payment.objects.suma_return(a.pk)
            elif a.asignation.detail_guide.magazine_day.day == '2':
                canillacero.miercoles =+ Payment.objects.suma_return(a.pk)
            elif a.asignation.detail_guide.magazine_day.day == '3':
                canillacero.jueves =+ Payment.objects.suma_return(a.pk)
            elif a.asignation.detail_guide.magazine_day.day == '4':
                canillacero.viernes =+ Payment.objects.suma_return(a.pk)
            elif a.asignation.detail_guide.magazine_day.day == '5':
                canillacero.sabado =+ Payment.objects.suma_return(a.pk)
            else:
                canillacero.domingo =+ Payment.objects.suma_return(a.pk)

        resultado.append(canillacero)
    return resultado


#funcion que devuelve el historial de una guia
def history_guide(guia):
    #recuperamos la guia y sus items
    detail_guides = DetailGuide.objects.filter(
        guide__pk=guia,
        guide__anulate=False,
        anulate=False,
        discount=False,
    )
    #para cada item calculamos histori guide
    resultado = []
    for item in detail_guides:
        #recuperamos el historial del detail guide
        hg = HistoryG()
        hg.pk = item.pk
        hg.magazine = item.magazine_day.magazine.name+'['+item.magazine_day.get_day_display()+']'
        hg.count_reception = item.count
        hg.precio_venta = item.precio_unitario
        hg.count_deliver = DetailAsignation.objects.suma_entregado(item)

        #recuperamos el resumen
        res = Payment.objects.resumen_historia(item.pk)
        tienda = Venta.objects.ventas_detail_guide(item.pk)
        hg.count_vendido = res['count_vendido'] + tienda
        hg.count_deuda = hg.count_deliver - res['count_vendido'] - res['count_devuelto']
        #hg.count_almacen = (item.count - hg.count_deliver) + (res['count_devuelto'] - tienda)
        hg.count_almacen = (
            (item.count - hg.count_deliver) + (res['count_devuelto']-tienda)
        )
        hg.total_almacen = hg.count_almacen*item.precio_unitario
        hg.total_vendido = hg.count_vendido*item.precio_unitario
        hg.total_deuda = hg.count_deuda*item.precio_unitario
        hg.count_real = item.real_count
        #recuperamo el historal del detalle guia
        h_d_g = Payment.objects.historial_detalle_guia(item.pk)
        #iteramos movimientos
        hg.historia = []
        devuelto = 0
        for h in h_d_g:
            history_g = HistoryGuide()
            history_g.count_dev = h['count_dev']
            history_g.count_ven = h['count_ven']
            history_g.date = h['date']
            devuelto = devuelto + history_g.count_dev
            #
            hg.historia.append(history_g)
        hg.count_devuelto = devuelto
        #agregamos venta en tienda
        aux_history = HistoryGuide()
        aux_history.count_dev = 0
        aux_history.count_ven = 0
        aux_history.count_tie = Venta.objects.ventas_detail_guide(item.pk)
        hg.historia.append(aux_history)

        resultado.append(hg)

    return resultado

def resumen_guia(date1,date2):
    #reuperamos la guias
    guias = Guide.objects.search_guides_date(date1,date2)
    resultado = []
    #para cada guia creamos objeto guia y resumen detalle guia
    for g in guias:
        rg = ResumenGuia()
        rg.number = g.number
        rg.provider = g.provider.name
        rg.date = g.date
        rg.culmined = g.culmined
        rg.amount_perdida = 0
        rg.itmes = []
        #recuperamos el resumen de itms de la guia
        detalle_guia = DetailGuide.objects.filter(anulate=False,guide__pk=g.pk)
        for dg in detalle_guia:
            rdg = ResumenDetalleGuia()
            res = Payment.objects.resumen_historia(dg.pk)
            tienda = Venta.objects.ventas_detail_guide(dg.pk)
            #
            rdg.magazine = dg.magazine_day
            rdg.precio_venta = dg.precio_unitario
            rdg.count_reception = dg.count
            rdg.count_deliver = DetailAsignation.objects.suma_entregado(dg)
            rdg.count_diferencia = rdg.count_reception - rdg.count_deliver
            rdg.count_vendido = res['count_vendido']
            rdg.count_deuda = rdg.count_deliver - rdg.count_vendido - res['count_devuelto']
            rdg.count_devuelto = res['count_devuelto'] - tienda
            rdg.count_almacen = dg.count - rdg.count_deliver + res['count_devuelto'] - tienda
            rdg.count_perdida = dg.real_count
            #
            rdg.total_almacen = rdg.count_almacen*dg.precio_unitario
            rdg.total_vendido = rdg.count_vendido*dg.precio_unitario
            rdg.total_deuda = rdg.count_deuda*dg.precio_unitario
            rdg.amount_perdida = rdg.count_perdida*dg.precio_unitario
            #
            rg.amount_perdida = rg.amount_perdida + rdg.amount_perdida
            rg.itmes.append(rdg)
        resultado.append(rg)
    return resultado
