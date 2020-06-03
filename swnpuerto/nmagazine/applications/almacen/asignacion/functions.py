# -*- encoding: utf-8 -*-
from datetime import datetime, timedelta
from decimal import Decimal
import operator
from django.utils import timezone

from applications.almacen.recepcion.models import DetailGuide
from applications.almacen.entidad.models import Vendor
from .models import DetailAsignation, Asignation, Pauta, DetailPauta, Receptors
from applications.caja.pagos.models import Payment


#creamos calse que rpresenta una pauta

class Pauta():
    diario = ''
    guia = ''
    pk = ''
    cod = ''
    name = ''
    tipo = ''
    count = 0
    mje = ""
    date = ''

class Consulta():
    pk = ''
    cod = ''
    name = ''
    count = 0
    returned = 0
    total = 0
    total_returned = 0
    diario = ''
    date = ''
    receptor = ''


class PautaMultiple():
    pk = ''
    cod =''
    name = ''
    count = []
    product = []


class Ponderado():
    canilla = ''
    valor = 0


class PautaProducto():
    magazine = ''
    precio_venta = 0
    count = 0


def generar_consulta(pk):
    #recuperamso la asigancion
    asig = Asignation.objects.get(pk=pk)
    #recuperamos la lista de canillas
    canillas = Vendor.objects.filter(
        disable=False,
        anulate=False,
    )
    resultado = []
    sum_total = 0
    sum_returned = 0
    #generamos lista resultado
    for c in canillas:
        dasig = DetailAsignation.objects.filter(
            vendor=c,
            asignation=asig,
            anulate=False,
        )
        if dasig.count() > 0:
            #creamos la pautas
            consulta = Consulta()
            consulta.diario = asig.detail_guide.magazine_day
            consulta.date = asig.detail_guide.created.date()
            consulta.pk = c.pk
            consulta.cod = c.cod
            consulta.name = c.name
            consulta.count = dasig[0].count
            consulta.returned = Payment.objects.suma_return(dasig[0].pk)
            if Receptors.objects.filter(detail_asignation=dasig).exists():
                consulta.receptor = Receptors.objects.filter(
                    detail_asignation=dasig,
                    anulate=False
                ).order_by('-created')[0].dni
            sum_total = sum_total + dasig[0].count
            sum_returned = sum_returned + Payment.objects.suma_return(dasig[0].pk)

            resultado.append(consulta)
        else:
            print 'error: no existe la consulta'

    resultado[0].total_returned = sum_returned
    resultado[0].total = sum_total
    return resultado


#funcion para generar valor ponderado de cada canilla
def generar_ponderado(pk_magazine):
    #recupramos lista de canillas
    tz = timezone.get_current_timezone()

    end_date = timezone.now()
    start_date = end_date - timedelta(days=30)

    canillas = Vendor.objects.filter(
        anulate=False,
        type_vendor='0',
        disable=False,
    )
    #inicializamos arreglo resultado
    resultado = []
    #recuperamos las tres ultimas asignaciones para cada canilla
    for c in canillas:
        asignations = DetailAsignation.objects.filter(
            anulate=False,
            created__range=(start_date, end_date),
            asignation__detail_guide__magazine_day__pk=pk_magazine,
            vendor=c,
        ).order_by('-created')[:3]
        p = Ponderado()
        #calculamos un valor ponderado
        if len(asignations) > 2:
            #calculamos el ponderado suamndo las tres asignaciones
            valores = [
                asignations[0].count - Payment.objects.suma_return(asignations[0].pk),
                asignations[1].count - Payment.objects.suma_return(asignations[1].pk),
                asignations[2].count - Payment.objects.suma_return(asignations[2].pk),
            ]
            ponderado = (valores[0] + valores[1] + valores[2])//3
            #creamos el objeto Ponderado
            p.canilla = c
            p.valor = ponderado

        else:
            p.canilla = c
            p.valor = 1

        resultado.append(p)

    #devolvemos el resultado
    return resultado

#funcoon que distribuye una cantidad (cantidad sobrannte)
def distribuir_difrencia(diferencia,lista,aux):
    #ordenamos la lista
    lista.sort(key = operator.attrgetter('count'))
    if aux == '0':
        i = 0
        while diferencia > 0:
            lista[i].count = lista[i].count + 1
            i = i + 1
            diferencia = diferencia - 1
    else:
        i = 0
        while diferencia > 0:
            lista[i].count = lista[i].count - 1
            i = i + 1
            diferencia = diferencia - 1

    lista.sort(key = operator.attrgetter('pk'))
    return lista

#funcion para generar pauta de un diario
def generar_pauta_fija(detail_guide):
    #generamos los valores ponderados
    canillas = generar_ponderado(detail_guide.magazine_day.pk)
    #realizamos la distribucion
    suma_ponderado = 0
    #calculamos la suma ponderado (suma total de ecuacion)
    for c in canillas:
        suma_ponderado = suma_ponderado + c.valor
    #calculamos el valor de la constante k=cantidad/suma_ponderado
    cte = Decimal(detail_guide.count)/Decimal(suma_ponderado)
    #realizamos distribucion entera segun cte
    resultado = []
    for canilla in canillas:
        pauta = Pauta()
        pauta.diario = detail_guide.magazine_day
        pauta.guia = detail_guide.guide.number
        pauta.date = detail_guide.created.date()
        pauta.pk = canilla.canilla.pk
        pauta.cod = canilla.canilla.cod
        pauta.name = canilla.canilla.name + ' ('+canilla.canilla.seudonimo+')'
        pauta.tipo = canilla.canilla.get_type_vendor_display
        pauta.count = int(round(cte*canilla.valor,0))
        #agregamos a un arreglo resultado
        resultado.append(pauta)

    #verificamos si la suma cubre la cantidad total
    suma = 0
    for r in resultado:
        suma = suma + r.count

    #redistribuimos cantidad sobrante
    if detail_guide.count != suma:
        if detail_guide.count > suma:
            diferencia = detail_guide.count - suma
            res = distribuir_difrencia(diferencia,resultado,'0')
        else:
            diferencia = suma - detail_guide.count
            res = distribuir_difrencia(diferencia,resultado,'1')

        return res
    else:
        #devolvemos el resultado
        return resultado


#funcion que devulve la ultima asignacion de un magazine
def cargar_asignacion(pk_dg):
    #verificamos si no existen pagos para detail guide
    pagos = Payment.objects.filter(
        anulate=False,
        detail_asignation__asignation__detail_guide=pk_dg,
    )
    resultado = []
    #si no tiene pagos
    if len(pagos)<1:
        print 'no tiene pagos'
        #ultima asignacion
        asignaciones = DetailAsignation.objects.filter(
            asignation__detail_guide=pk_dg,
            anulate=False,
        ).order_by('vendor__cod')
        #devolvemos las asignaciones
        for a in asignaciones:
            pauta = Pauta()
            pauta.diario = pk_dg.magazine_day
            pauta.date = pk_dg.created.date()
            pauta.pk = a.vendor.pk
            pauta.cod = a.vendor.cod
            pauta.name = a.vendor.name
            pauta.count = a.count
            pauta.tipo = a.vendor.get_type_vendor_display
            pauta.mje = 'Consulta Exitosa'
            resultado.append(pauta)
    else:
        print 'tiene pagos'
        pauta = Pauta()
        pauta.diario = '-'
        pauta.pk = '0'
        pauta.cod = '0'
        pauta.name = '-'
        pauta.count = 0
        pauta.tipo = '-'
        pauta.mje = 'No se Puede Modificar la Asignacion Por que, ya se registraron pagos'
        resultado.append(pauta)
    return resultado

def cargar_pauta(pk_dg):
    #ultima asignacion
    asignaciones = DetailPauta.objects.filter(
        pauta__detail_guide=pk_dg,
    ).order_by('vendor__cod')
    print '*****************'
    print asignaciones.count()
    resultado = []
    #devolvemos las asignaciones
    for a in asignaciones:
        pauta = Pauta()
        pauta.diario = pk_dg.magazine_day
        pauta.date = pk_dg.created.date()
        pauta.pk = a.vendor.pk
        pauta.cod = a.vendor.cod
        pauta.name = a.vendor.name
        pauta.count = a.count
        pauta.tipo = a.vendor.get_type_vendor_display
        pauta.mje = 'Consulta Exitosa'
        resultado.append(pauta)

    return resultado

def generar_pauta_dinamica(dia):
    # recuepramos lista de canillas
    canillas = Vendor.objects.filter(
        anulate=False,
        type_vendor='0',
        disable=False,
    ).order_by('cod')
    #recuperamos la lista de diarios
    lista = DetailGuide.objects.diarios_by_dia(dia)
    #creamos arreglo de pautas
    pautas = []
    # creamos arreglo resultado
    resultado = []

    for dg in lista:
        #para cada diario generamos su lista de canillas
        pauta = generar_pauta_fija(dg)
        pautas.append(pauta)

    #recorremos la matriz pautas
    i = 0
    for c in canillas:
        p = PautaMultiple()
        p.pk = c.pk
        p.cod = c.cod
        p.name = c.name
        p.count =[]
        p.product =[]
        #agregamos las cantidades
        for pta in pautas:
            p.count.append(pta[i].count)

        #agregamos los diarios
        for dg in lista:
            p.product.append(dg.magazine_day.magazine.name)

        i = i + 1
        resultado.append(p)

    return resultado


#funcion que devuelve la pauta de prouctos de un canilla
# def pauta_prod_canilla(cod):
#     #recuperamos los detalles pauta del canilla
#     pautas = DetailPauta.objects.filter(
#         vendor__cod=cod,
#         asignado=False,
#     )
