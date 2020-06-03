# -*- encoding: utf-8 -*-
from datetime import datetime

from django.db.models import Q

from applications.almacen.recepcion.models import DetailGuide, Guide
from applications.almacen.entidad.models import Vendor

from applications.caja.pagos.models import Payment, Invoce, Venta

from applications.caja.pagos.functions import verificar_vencimiento


#objeto que representa un magazine
class Producto():
    pk_diario = ''
    diario = ''
    time = ''
    devuelto = 0
    pagado = 0
    monto = 0


#objeto que representa un movimiento
class MovimientosCanilla():
    name = ''
    cod = ''
    seudonimo = ''
    total = 0
    movimientos = []

class Movimientos():
    magazine = ''
    dia = ''
    date = ''
    entregado = 0
    devuelto = 0
    pagado = 0
    debe = 0
    precio = 0
    #monto_deuda = 0
    amount = 0

#objeto que representa un detalle de guia liquidada
class LiquidacionGuia():
    factura = ''
    guide = ''
    magazine = ''
    date = ''
    count = ''
    amount_total = 0
    precio_unitario = 0
    devuelto = 0
    vendido = 0
    amount_vendido = 0
    provider = ''
    amount = ''
    total = 0

class LiquidacionProveedor():
    name = '',
    sub_total = 0
    lista_pagos = []

class ResumenPagos():
    guide = ''
    date = ''
    magazine = ''
    dia = ''
    precio = 0
    devuelto = 0
    pagado = 0
    total = 0


#objeto que representa un detalle de guia liquidada
class GuiaDetalle():
    magazine_day = ''
    count = 0
    precio_guia = 0
    precio_venta = 0
    devuelto = 0
    vendido = 0


#objeto que representa una guia
class Guia():
    number = ''
    date = ''
    number_invoce = ''
    provider = ''
    detalle = []


#representamos un pago

def vencido(canilla,magazine_day, fecha):
    #funcion para verificar si un diairo vencio
    dias = DetailGuide.objects.magazin_days_date(magazine_day.pk,fecha)
    if dias >= canilla.plazo:
        return False
    else:
        return True


#funcion que devuelve deudas y pagos de canillas
def movimientos_caja(fecha):
    #recuperamos la lista de canillas
    canillas = Payment.objects.list_vendors_day(fecha)

    resultado = []
    #iteramos canillas
    for c in canillas:
        mc = MovimientosCanilla()
        mc.cod = c['codigo']
        mc.name = c['detail_asignation__vendor__name']
        mc.seudonimo = c['detail_asignation__vendor__seudonimo']
        mc.total = c['monto']
        mc.movimientos = Payment.objects.mov_caja_day(fecha,mc.cod)
        resultado.append(mc)
    return resultado


#funcion que genera liquidacion por guia
def liquidacion_guia(date1,date2, provider):
    fecha1 = datetime.strptime(date1, '%d-%m-%Y').date()
    fecha2 = datetime.strptime(date2, '%d-%m-%Y').date()
    #recuperamos la lista de guias segun fecha y proveedor
    if len(provider) > 0:
        guias = Guide.objects.guias_by_date_range(fecha1,fecha2).filter(
            provider__pk=provider,
        )
    else:
        guias = Guide.objects.guias_by_date_range(fecha1.fecha2)

    #creamos variable resultado
    resultado = []
    #iteramos la guias y recuperamos sus detalles

    #iteramos la guias
    for g in guias:
        total = 0
        sub_total = 0
        #recuperamos los detalles d ela guia
        details = DetailGuide.objects.filter(
            anulate=False,
            guide=g,
        )
        #iteramos los detalle guia
        i = 0
        while i < len(details):
            dg = details[i]
            guia = LiquidacionGuia()
            guia.factura = g.number_invoce
            guia.guide = g.number
            guia.date = g.date
            guia.provider = str(g.provider)[:6]
            guia.magazine = str(dg.magazine_day)[:15]
            guia.count = dg.count
            guia.precio_unitario = dg.precio_guia
            guia.amount_total = dg.count*dg.precio_guia
            guia.devuelto = Payment.objects.suma_return_guide(dg)
            guia.vendido = Payment.objects.suma_payment_guide(dg)
            guia.amount_vendido = guia.vendido*dg.precio_guia
            #calculamos sub total
            sub_total = sub_total + guia.amount_vendido

            if i == len(details) -1:
                guia.amount = str(sub_total)
            else:
                guia.amount = ' '

            i = i + 1

            resultado.append(guia)

    return resultado


#funcion que genera liquidacion por guia detallada
def liquidacion_guia_detalle(date1,date2):
    fecha1 = datetime.strptime(date1, '%d-%m-%Y').date()
    fecha2 = datetime.strptime(date2, '%d-%m-%Y').date()
    #recuperamos la lista de guias segun fecha
    guias = Guide.objects.guias_by_date_range(fecha1,fecha2)
    #creamos variable resultado
    resultado = []
    #iteramos la guias y recuperamos sus detalles
    for g in guias:
        #creamos el objeto guia
        guia = Guia()
        guia.number = g.number
        guia.date = g.date
        guia.number_invoce = g.number_invoce
        guia.provider = g.provider
        guia.detalle = []
        #creamos el detalle
        detail_guides = DetailGuide.objects.filter(
            anulate=False,
            guide=g,
        )
        #iteramos los detalles
        for dg in detail_guides:
            #creamos objeto Guia Detalle
            guia_detalle = GuiaDetalle()
            guia_detalle.magazine_day = dg.magazine_day
            guia_detalle.count = dg.count
            guia_detalle.precio_guia = dg.precio_guia
            guia_detalle.precio_venta = dg.precio_unitario
            guia_detalle.devuelto = Payment.objects.suma_return_guide(dg)
            guia_detalle.vendido = Payment.objects.suma_payment_guide(dg)
            guia.detalle.append(guia_detalle)

        resultado.append(guia)
    return resultado


#funcion que devuelve la liquidacion diaria de caja
def liquidacion_by_day(date):
    fecha = datetime.strptime(date, '%d-%m-%Y').date()
    #recuperamos guias no culminadas
    guias = Guide.objects.filter(
        anulate=False,
    )
    resultado = []
    for g in guias:
        #recuperamos pagos del dia
        pagos = Payment.objects.payment_by_guide(g).filter(
            created__date=fecha,
        ).filter(Q(count_return__gt=0) | Q(count_payment__gt=0))

        #iteramos los pagos
        sub_total = 0
        i = 0
        while i < len(pagos):
            p = pagos[i]
            pago = LiquidacionGuia()
            pago.guide = g.number
            pago.date = p.created.date()
            pago.magazine = str(p.detail_asignation.asignation.detail_guide.magazine_day)[:14]
            pago.count = p.detail_asignation.count
            pago.devuelto = p.count_return
            pago.vendido = p.count_payment
            pago.precio_unitario = p.detail_asignation.precio_venta
            pago.amount_vendido = p.amount

            sub_total = sub_total + pago.amount_vendido

            if i == len(pagos) - 1:
                pago.amount = str(sub_total)
            else:
                pago.amount = ' '

            resultado.append(pago)

            i = i + 1

    return resultado


def liquidacion_por_day(date):
    fecha = datetime.strptime(date, '%d-%m-%Y').date()
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
    #recuperamos lo pagos registrados en la fecha
    pagos_resumen = Payment.objects.cuadre_caja_guia(fecha)
    #recuperamos los Proveedores
    list_proveedores = []
    for prov in pagos_resumen:
        if not prov['proveedor'] in list_proveedores:
            list_proveedores.append(prov['proveedor'])

    #iteramos y creamos el objeto liquidacion proveedor
    resultado = []
    for p in list_proveedores:
        obj = LiquidacionProveedor()
        obj.name = p
        obj.sub_total = 0
        obj.lista_pagos = []
        for pago in pagos_resumen:
            if pago['proveedor'] == p:
                obj.sub_total = obj.sub_total + pago['total']
                #creamos el objeto pago
                resumen_pagos = ResumenPagos()
                resumen_pagos.guide = pago['guia']
                resumen_pagos.date = pago['detail_asignation__asignation__detail_guide__guide__date']
                resumen_pagos.magazine = pago['magazine']
                resumen_pagos.dia = DAY_CHOICES[pago['dia']]
                resumen_pagos.precio = pago['detail_asignation__asignation__detail_guide__precio_unitario']
                resumen_pagos.devuelto = pago['devuelto'] - Venta.objects.guide_vendido(pago['detail_asignation__asignation__detail_guide'],fecha)
                resumen_pagos.pagado = pago['pagado']
                resumen_pagos.total = pago['total']
                obj.lista_pagos.append(resumen_pagos)

        resultado.append(obj)

    #recuperamos ventas de caja
    ventas = Venta.objects.cuadre_ventas(fecha)
    if ventas.count() > 0:
        obj_ventas = LiquidacionProveedor()
        obj_ventas.name = '[VENTA-CAJA]'
        obj_ventas.sub_total = 0
        obj_ventas.lista_pagos = []
        for v in ventas:
            obj_ventas.sub_total = obj_ventas.sub_total + v['total']
            #creamos el objeto pago
            resumen_pagos = ResumenPagos()
            resumen_pagos.guide = "VENTA-CAJA"
            resumen_pagos.date = v['detail_guide__guide__date']
            resumen_pagos.magazine = v['magazine']
            resumen_pagos.precio = v['detail_guide__precio_unitario']
            resumen_pagos.dia = '[VENTA-CAJA]'
            resumen_pagos.pagado = v['vendido']
            resumen_pagos.total = v['total']
            obj_ventas.lista_pagos.append(resumen_pagos)

        resultado.append(obj_ventas)

    return resultado
