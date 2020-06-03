# -*- encoding: utf-8 -*-
import operator
from datetime import datetime
from applications.almacen.asignacion.models import DetailAsignation
from applications.almacen.recepcion.models import Guide, DetailGuide
from applications.almacen.entidad.models import Vendor
from .models import Payment, Invoce


#clase que representa un pago
class Pago():
    estado = 'CONFORME'
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
    #boleta = len(Invoce.objects.all())
    vencido = False
    por_vencer = []
    date = ''


class Diarios():
    diario = ''
    cantidad = 0
    por_vencer = False


class CuadrarCaja():
    date = ''
    magazine = ''
    tipo = ''
    devuelto = 0
    cantidad = 0
    precio_venta = 0
    monto = 0


class Devolucion():
    magazine = ''
    boleta = ''
    cantidad = ''


class DetalleCuadrar():
    amount = 0
    cantidad = 0
    payment = ''
    count_return = 0


class ProdVenta():
    pk = ''
    magazine = ''


#funcion que devuelve canillas en tope
def tope_canilla(pk_canilla):
    #recuperamos el canilla
    canilla = Vendor.objects.get(pk=pk_canilla)
    #recuperamos los darios para el canilla aun no pagados
    lista_diarios = DetailAsignation.objects.filter(
        culmined=False,
        vendor=canilla,
    )
    #iteramos lista de diarios en no culminados
    total = 0
    for ld in lista_diarios:
        #obtenemos la canidades
        deuda = ld.count - Payment.objects.suma_payment(ld.pk)
        total = total + deuda*ld.precio_venta

    if total >= canilla.line_credit:
        return True
    else:
        return False

#funcion ue devuleve una matriz de pagos
def pagos_canilla(pk_canilla):
    #recuperamos el canilla
    canilla = Vendor.objects.get(cod=pk_canilla)
    #recuperamos los darios para el canilla aun no pagados
    lista_diarios = DetailAsignation.objects.filter(
        culmined=False,
        vendor=canilla,
    )
    diarios_cantidad = []
    #para elemento de la lista calculamos los pagos
    for ld in lista_diarios:
        #verificamo si producto vencio
        tipo = ld.asignation.detail_guide.magazine_day.magazine.tipo
        detail_guide = ld.asignation.detail_guide
        #cargamos diarios a figurar en caja
        if (((tipo=='1') and (verificar_por_cobrar(canilla,detail_guide)))or(tipo=='0')):
            d = Diarios()
            #obtenemos la canidades
            suma = ld.count - Payment.objects.suma_payment(ld.pk)
            d.diario = ld
            d.cantidad = suma
            diarios_cantidad.append(d)
        #cargamos diairos a figurara en cobranza del dia siguiente
        if ((tipo == '1') and (verificar_por_vencer(canilla,detail_guide))):
            d = Diarios()
            d.diario = ld
            d.por_vencer = True

    return diarios_cantidad


#funcion que devuelve la lista de magazine que debe un canillas
def deuda_magazine_canilla(cod_canilla):
    #recuperamos la lista de diarios que debe
    canilla = Vendor.objects.get(cod=cod_canilla)
    #recuperamos los darios para el canilla aun no pagados
    lista_diarios = DetailAsignation.objects.filter(
        culmined=False,
        asignation__detail_guide__anulate=False,
        vendor=canilla,
        count__gt=0,
    ).order_by('asignation__detail_guide__magazine_day__magazine__tipo')
    #
    #variable resultado final
    resultado = []
    #variable que almacena diarios por vener
    lis_por_vencer = []
    #para cada diarios calculamos la cantidad de deuda
    for ld in lista_diarios:
        #verificamo si producto vencio
        tipo = ld.asignation.detail_guide.magazine_day.magazine.tipo
        detail_guide = ld.asignation.detail_guide

        #cargamos diairos a figurara en cobranza del dia siguiente
        if ((tipo == '1') and (verificar_por_vencer(canilla,detail_guide))):
            lis_por_vencer.append(detail_guide.magazine_day.magazine.name)

        #cargamos diarios a figurar en caja si cumple condicion
        if (((tipo=='1') and (verificar_por_cobrar(canilla,detail_guide)))or(tipo=='0')):
            p = Pago()
            #
            p.pk_asignation = ld.pk
            #
            if tipo == '1':
                p.diario = detail_guide.magazine_day.magazine.name
            else:
                p.diario = detail_guide.magazine_day
            #
            p.tipo = detail_guide.magazine_day.magazine.get_tipo_display()
            #
            p.canilla = canilla.name
            #
            p.guide = detail_guide.guide.number
            #
            p.entregado = ld.count - Payment.objects.suma_payment2(ld.pk)
            #
            #obtenemos la cantidad que se debe
            p.pagar = p.entregado
            #
            p.precio_venta = detail_guide.precio_unitario
            #
            p.amount = p.precio_venta*p.pagar
            #
            p.date = ld.created.date()
            #
            p.vencido =  verificar_vencimiento(canilla,detail_guide)
            if p.vencido:
                p.estado = 'VENCIDO'
            #
            p.por_vencer = lis_por_vencer

            #agregamos a resultado
            resultado.append(p)

    return resultado


def por_cobrar():
    #calculamos el monto por cobrar
    consulta = DetailAsignation.objects.filter(
        anulate=False,
        culmined=False,
    )
    monto = 0
    #recorremos consulta y calculamos monto
    for c in consulta:
        debe = c.count - Payment.objects.suma_payment(c.pk)
        monto = monto + debe*c.precio_venta

    return monto

def verificar_vencimiento(canilla, detail_guide):
    #funcion para verificar si un diairo vencio
    dias = DetailGuide.objects.dias_magazine(detail_guide.pk)
    if detail_guide.magazine_day.magazine.tipo == '1':
        if dias >= canilla.plazo - 1:
            return False
        else:
            return True
    else:
        if dias >= canilla.plazo:
            return False
        else:
            return True


def verificar_por_cobrar(canilla, detail_guide):
    ##verificamos si un producto ya se debe cobrar
    if detail_guide.magazine_day.magazine.tipo == '1':
        #dias que lleva registrado
        dias = DetailGuide.objects.dias_magazine(detail_guide.pk)
        # print '*******************'
        if dias <= canilla.plazo:
            return True
        else:
            print detail_guide
            return False
    else:
        return False


def verificar_por_vencer(canilla, detail_guide):
    ##verificamos si es producto y cuanto falta por vencer
    if detail_guide.magazine_day.magazine.tipo == '1':
        dias = DetailGuide.objects.dias_magazine(detail_guide.pk)
        if dias-1 == canilla.plazo:
            return True
        else:
            return False
    else:
        return False


def magazine_pago_canilla(codigo):

    #recuperamos la lista de diarios aun no cancelados
    diarios = pagos_canilla(codigo)
    #recuperamos la lsiat total de diarios
    lista1 = DetailAsignation.objects.magazine_by_vendor(codigo)
    #creamos lista auxiliar para comparaciones
    lista2 = diarios
    #recuperamos el canilla
    canilla = Vendor.objects.get(cod=codigo)
    resultado = []
    lis_por_vencer = []
    for magazine in lista1:
        #primero cargamos arrego de diaros por vencer
        if verificar_por_vencer(canilla,magazine.asignation.detail_guide):
            lis_por_vencer.append(magazine.asignation.detail_guide.magazine_day)

    #iteramos la lista inicial de diarios
    for magazine in lista1:

        magazine_day = magazine.asignation.detail_guide.magazine_day
        detail_guide = magazine.asignation.detail_guide
        entregado = 0
        precio_venta = 0
        date = ''
        #iteramos la lista auxiliar para comparar
        for diario in lista2:
            #recuperamos el codigo de diario
            l2 = diario.diario.asignation.detail_guide.pk
            #verificamos si se trata del mismo diario
            if magazine.asignation.detail_guide.pk == l2:
                precio_venta = diario.diario.precio_venta
                date = diario.diario.asignation.created.date()
                entregado += diario.cantidad

        #agregamos a resultado
        if entregado > 0:

            #creamos objeto pago
            pago = Pago()
            pago.por_vencer = lis_por_vencer
            pago.pk_diario = magazine_day.pk
            if magazine_day.magazine.tipo == '1':
                #si es producto devolvemos nombre
                pago.diario = magazine_day.magazine.name
            else:
                #si es diario devolvemos magzine day
                pago.diario = magazine_day

            pago.tipo = magazine_day.magazine.get_tipo_display()
            pago.entregado = entregado
            pago.canilla = canilla

            if magazine_day.magazine.tipo == '1':
                #si es producto inicializamos pagar con cero
                pago.devuelto = 0
                pago.deuda = 0
                pago.pagar = entregado
            else:
                pago.devuelto = 0
                pago.deuda = 0
                pago.pagar = entregado

            pago.precio_venta = precio_venta
            pago.amount = pago.precio_venta*pago.pagar
            pago.vencido = verificar_vencimiento(canilla, detail_guide)
            pago.date = date

            #devolvemos resultado
            resultado.append(pago)

    return resultado

#metodo para mostrar las lista de movimientos de caja
def lista_movimientos():
    magazines, consulta = Payment.objects.magazine_by_day()
    #creamos variable resultado
    resultado = []
    monto_total = 0
    #recorremos las listas
    for m in magazines:
        monto = 0
        cantidad = 0
        devuelto = 0
        date = ''
        precio_venta = 0
        #recorremos la segunda lista
        for c in consulta:
            #comparamos
            aux = c.detail_asignation.asignation.detail_guide
            if m == aux:
                date = c.detail_asignation.created.date()
                precio_venta = c.detail_asignation.precio_venta
                monto = monto + c.amount
                cantidad = cantidad + c.count_payment
                devuelto = devuelto + c.count_return

        #calculamos el monto total
        if monto > 0:
            monto_total = monto_total + monto
            caja = CuadrarCaja()
            caja.date = date
            caja.magazine = m.magazine_day
            caja.tipo = m.magazine_day.magazine.get_tipo_display()
            caja.devuelto = devuelto
            caja.cantidad = cantidad
            caja.precio_venta = precio_venta
            caja.monto = monto

            resultado.append(caja)

    return resultado, monto_total


def detalle_movimientos(consulta, boletas):
    #creamos la variable que contendra resultado
    resultado = []
    for b in boletas:
        monto = 0
        cantidad = 0
        payment = ''
        count_return = 0
        #rrecorremos las bolestas
        for c in consulta:
            if c.invoce == b:
                monto = monto + c.amount
                cantidad = cantidad + c.count_payment
                count_return = count_return + c.count_return
                payment = c

        detalleMov = DetalleCuadrar()
        detalleMov.amount = monto
        detalleMov.cantidad = cantidad
        detalleMov.payment = payment
        detalleMov.count_return = count_return
        resultado.append(detalleMov)

    return resultado

#funcion para listar las devoluciones de diarios
def devolucion_movimientos():
    magazines, consulta = Payment.objects.magazine_by_day()
    #creamos variable resultado
    resultado = []
    cantidad_total = 0
    #recorremos las listas
    for m in magazines:
        cantidad = 0
        voucher = ''
        #recorremos la segunda lista
        for c in consulta:
            #comparamos
            aux = c.detail_asignation.asignation.detail_guide.magazine_day
            if m == aux:
                cantidad = cantidad + c.count_return
                voucher = c.invoce.pk

        #calculamos el monto total
        cantidad_total = cantidad_total + cantidad
        devolucion = Devolucion()
        devolucion.magazine = m
        devolucion.cantidad = cantidad
        devolucion.boleta = voucher

        resultado.append(devolucion)

    return resultado, cantidad_total

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
    deuda = detail_asignation.count - Payment.objects.suma_payment2(detail_asignation.pk)
    if deuda <= 0:
        detail_asignation.culmined = True
        detail_asignation.save()
        print "******ASIGNACION CULMINADA******"
        print deuda

    #cerrar la guia
    cerrar_guia(detail_asignation.asignation.detail_guide.guide)

    return True


def listar_productos_venta():
    resultado = []
    #recuperamos los productos que se devolvieron en el dia
    fecha = datetime.now().date()
    pagos = Payment.objects.filter(
        anulate=False,
        created__date=fecha,
        detail_asignation__asignation__detail_guide__magazine_day__magazine__tipo='1',
    ).values(
        'detail_asignation__asignation__detail_guide__pk',
        'detail_asignation__asignation__detail_guide__magazine_day__magazine__name'
    ).distinct()

    #convertimos el resultado
    for p in pagos:
        prodventa = ProdVenta()
        prodventa.pk = p['detail_asignation__asignation__detail_guide__pk']
        prodventa.magazine = p['detail_asignation__asignation__detail_guide__magazine_day__magazine__name']
        resultado.append(prodventa)
    return resultado


def deuda_detail_guide_vendor(guide):
    """ funcion que devuelve lista de magazines que debe un canillas """

    asignation_vendors = DetailAsignation.objects.filter(
        culmined=False,
        anulate=False,
        asignation__detail_guide__anulate=False,
        asignation__detail_guide__guide__number=guide,
    )
    resultado = []
    for a in asignation_vendors:
        deuda = a.count - Payment.objects.suma_payment2(a.pk)
        if deuda > 0:
            vendor = {
                'cod':a.vendor.cod,
                'vendor':a.vendor,
                'date':a.created,
                'magazine':a.asignation.detail_guide.magazine_day,
                'deuda':deuda
            }
            resultado.append(vendor)

    return resultado




#============================  SCRIP AUXILIARES PARA NIVELAR SISTEMA=====================================================
def culminar_detalle_asignaciones():
    detail_asignations = DetailAsignation.objects.filter(
        culmined=False,
    )
    for da in detail_asignations:
        if (da.count - Payment.objects.suma_payment2(da.pk)) <=0:
            da.culmined = True
            da.save()
        else:
            da.culmined = False
            da.save()

    return True


#funcion para cerrar un guia
def cerrar_guia(guide):
    #recuperamos la deuda totoal de la guia
    if Payment.objects.deuda_by_guide(guide) <= 0:
        guide.culmined = True
        guide.save()
        print '===EL PAGO HA CERRADO LA GUIA==='
    else:
        guide.culmined = False
        guide.save()
        print 'AUN NO SE HA CERRADO LA GUIA'


#funcion para cerrar guias canceladas
def cerrar_guias():
    #recuperamos guias no cerradas
    guias = Guide.objects.filter(
        anulate=False,
        culmined=False,
    )
    #para cada guia recuperamos la deuda total
    for g in guias:
        #recperamos la deuda
        if Payment.objects.filter(anulate=False,detail_asignation__asignation__detail_guide__guide=g).exists():
            if Payment.objects.deuda_by_guide(g) <= 0:
                g.culmined = True
                g.save()
                print
                print '===GUIA CERRADA==='
        else:
            print 'la guia no tiene pagos'

    return True


def cerrar_activar_guias():
    #recuperamos guias no cerradas
    guias = Guide.objects.filter(
        anulate=False,
    )
    print '==========='
    print guias.count()
    #para cada guia recuperamos la deuda total
    for g in guias:
        #verificamos si tiene pagos
        if Payment.objects.filter(anulate=False,detail_asignation__asignation__detail_guide__guide=g).exists():
            if Payment.objects.deuda_by_guide(g) <= 0:
                g.culmined = True
                g.save()
                print '===GUIA CERRADA==='
            else:
                print '===GUIA NO CERRADA==='
                g.culmined = False
                g.save()
        else:
            g.culmined = False
            g.save()
            print 'La Guia aun no Tiene Pagos'

    return True
