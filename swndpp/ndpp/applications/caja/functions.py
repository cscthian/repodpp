# -*- encoding: utf-8 -*-
import operator
from datetime import datetime, timedelta
from applications.recepcion.models import (
    DetailAsignation,
    Guide,
    DetailGuide,
)
from applications.miscelanea.models import Vendor
from .models import Payment, Invoce


#clase que representa un pago
class Pago():
    guide = ''
    pk_asignation = ''
    diario = ''
    tipo = ''
    canilla = ''
    entregado = 0
    devuelto = 0
    pagar = 0
    deuda = 0
    precio_venta = 0.000
    amount = 0.000
    number_operation = ""
    date_operation = ""
    date = ""
    vencido = ""


class Diarios():
    diario = ''
    cantidad = 0
    por_vencer = False


#formato liquidacion proveedor
class LiquidacionProveedor():
    name = ''
    monto_deuda = 0
    cerradas = 0
    no_cerradas = 0
    sub_total = 0
    lista_pagos = []

#formato resumen de los pagos copbrdos
class ResumenPagos():
    guide = ''
    date = ''
    magazine = ''
    dia = ''
    estado = ''
    precio = 0
    devuelto = 0
    debe = 0
    pagado = 0
    total = 0


#funcion que devuelve la lista de magazine que debe un canillas por guia
def deuda_magazine_agente(codigo):
    #recuperamos la guia enviada
    vendor = Vendor.objects.get(cod=codigo)
    #recuperamos la fecha actual para ver si debe figurar en cobranza
    hoy = datetime.now().date()
    #recuperamos los darios para la guia
    lista_diarios = DetailAsignation.objects.filter(
        culmined=False,
        asignation__detail_guide__anulate=False,
        asignation__detail_guide__guide__date_cobranza__lte=hoy,
        vendor=vendor,
        count__gt=0,
        anulate=False,
    ).order_by('asignation__detail_guide__magazine_day__magazine__tipo')
    #
    #variable resultado final
    resultado = []
    #para cada diarios calculamos la cantidad de deuda
    for ld in lista_diarios:
        #verificamo si producto vencio
        tipo = ld.asignation.detail_guide.magazine_day.magazine.tipo
        detail_guide = ld.asignation.detail_guide

        #cargamos diarios a figurar en caja
        p = Pago()
        #
        p.pk_asignation = ld.pk
        #
        if tipo == '1':
            p.diario = detail_guide.magazine_day.magazine.name
        else:
            p.diario = detail_guide.magazine_day.magazine.name + '['+detail_guide.magazine_day.get_day_display()+']'
        #
        p.tipo = detail_guide.magazine_day.magazine.get_tipo_display()
        #
        p.canilla = ld.vendor.name
        #
        p.guide = detail_guide.guide.number
        #
        p.entregado = ld.count - Payment.objects.suma_payment(ld.pk)
        #
        #obtenemos la cantidad que se debe
        p.pagar = p.entregado
        #
        p.precio_venta = detail_guide.precio_unitario
        #
        p.amount = p.precio_venta*p.pagar
        #
        p.date = ld.asignation.detail_guide.guide.date_emission
        #verificamos si el producto ya vencio
        new_date = hoy - timedelta(days=2)
        if ld.asignation.detail_guide.guide.date_cobranza < new_date:
            p.vencido = "VENCIDO"
        else :
            p.vencido = "---"
        #agregamos a resultado
        resultado.append(p)

    return resultado

#
#funcion que devuelve la lista de magazine que debe un canillas por guia
def deuda_magazine_agente_detalle(codigo):
    #recuperamos la guia enviada
    vendor = Vendor.objects.get(cod=codigo)
    #recuperamos la fecha actual para ver si debe figurar en cobranza
    hoy = datetime.now().date()
    #recuperamos los darios para la guia
    lista_diarios = DetailAsignation.objects.filter(
        culmined=False,
        asignation__detail_guide__anulate=False,
        asignation__detail_guide__guide__date_cobranza__lte=hoy,
        vendor=vendor,
        count__gt=0,
        anulate=False,
    ).order_by('asignation__detail_guide__magazine_day__magazine__tipo')
    #
    #variable resultado final
    resultado = []
    #para cada diarios calculamos la cantidad de deuda
    for ld in lista_diarios:
        #verificamo si producto vencio
        tipo = ld.asignation.detail_guide.magazine_day.magazine.tipo
        detail_guide = ld.asignation.detail_guide

        #cargamos diarios a figurar en caja
        p = Pago()
        #
        p.pk_asignation = ld.pk
        #
        if tipo == '1':
            p.diario = detail_guide.magazine_day.magazine.name
        else:
            p.diario = detail_guide.magazine_day.magazine.name + '['+detail_guide.magazine_day.get_day_display()+']'
        #
        p.tipo = detail_guide.magazine_day.magazine.get_tipo_display()
        #
        p.canilla = ld.vendor.name
        #
        p.guide = detail_guide.guide.number
        #
        p.entregado = ld.count - Payment.objects.suma_payment(ld.pk)
        #
        #obtenemos la cantidad que se debe
        p.pagar = p.entregado
        #
        p.precio_venta = detail_guide.precio_unitario
        #
        p.amount = p.precio_venta*p.pagar
        #
        p.date = ld.asignation.detail_guide.guide.date_emission
        #
        p.vencido = str((hoy - p.date).days) + ' Dias'
        #agregamos a resultado
        resultado.append(p)

    return resultado


#deuda magaine agente suma totol
def deuda_magazine_agente_total(codigo):
    consulta = deuda_magazine_agente(codigo)
    #
    suma = 0
    for c in consulta:
        suma = suma + c.amount

    return suma

#funcion que actualiza devoluciones y registra pagos
def registrar_pagos(detail_asignation,factura, pagar, devuelto, usuario):
    #regitramos el pago y devolucion para el detail asignation
    amount = detail_asignation.precio_venta * pagar
    pago = Payment(
        detail_asignation=detail_asignation,
        invoce=factura,
        count_payment=pagar,
        count_return=devuelto,
        amount=amount,
        date=datetime.now().date(),
        user_created=usuario,
    )
    pago.save()
    #verificamos si ya completo el pago
    deuda = detail_asignation.count - Payment.objects.suma_payment(detail_asignation.pk)
    if deuda <= 0:
        detail_asignation.culmined = True
        detail_asignation.save()
        print "******ASIGNACION CULMINADA******"
        print deuda

    #bloquear canillas

    return True


def liquidacion_por_day(fecha):
    if fecha == '':
        fecha = datetime.now().date()

    print '********'
    print fecha

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
        obj.monto_deuda = 0
        obj.cerradas = 0
        obj.no_cerradas = 0
        obj.lista_pagos = []
        for pago in pagos_resumen:
            if pago['proveedor'] == p:
                obj.sub_total = obj.sub_total + pago['total']
                #creamos el objeto pago
                resumen_pagos = ResumenPagos()
                resumen_pagos.guide = pago['guia']
                #asignamos le estado
                if Guide.objects.get(number=pago['guia']).culmined == True:
                    resumen_pagos.estado = 'C'
                    obj.cerradas = 1
                else:
                    resumen_pagos.estado = 'N'
                    obj.no_cerradas = 1
                #
                resumen_pagos.date = pago['detail_asignation__asignation__detail_guide__guide__date']
                resumen_pagos.magazine = pago['magazine']
                resumen_pagos.dia = DAY_CHOICES[pago['dia']]
                resumen_pagos.entregado = pago['detail_asignation__asignation__detail_guide__count']
                resumen_pagos.debe = (
                    pago['detail_asignation__asignation__detail_guide__count'] - Payment.objects.suma_payment(pago['detail_asignation__asignation__detail_guide'])
                )
                resumen_pagos.precio = pago['detail_asignation__asignation__detail_guide__precio_unitario']
                resumen_pagos.devuelto = pago['devuelto']
                resumen_pagos.pagado = pago['pagado']
                resumen_pagos.total = pago['total']
                obj.monto_deuda = obj.monto_deuda + (resumen_pagos.debe*resumen_pagos.precio)
                obj.lista_pagos.append(resumen_pagos)

        resultado.append(obj)
    return resultado


def resumen_liquidacion(fecha):
    #recuperaos la liquidacon
    liquidacion = liquidacion_por_day(fecha)
    #recorremos el resultado y obtenemos el resumen
    monto_cal = 0
    deuda_tot = 0
    cerradas = 0
    no_cerradas = 0
    #
    for l in liquidacion:
        monto_cal = monto_cal + l.sub_total
        deuda_tot = deuda_tot + l.monto_deuda
        cerradas = cerradas + l.cerradas
        no_cerradas = no_cerradas + l.no_cerradas
    #agregamos lo resultados
    return {
        'monto_cal':monto_cal,
        'deuda_tot':deuda_tot,
        'cerradas':cerradas,
        'no_cerradas':no_cerradas
    }
