from datetime import datetime, timedelta
#app recpecion
from applications.recepcion.models import Guide, DetailGuide, DetailAsignation

#app miscelanea
from applications.miscelanea.models import Departamento

#app caja
from applications.caja.models import Payment

#app reporte
from applications.reportes.models import DetailVoucher, Voucher

#app admini
from .models import DetailBoleta


#clase que representa un objeto liquidacion proveedor

class LidacionProveedor():
    number = ''
    factura = ''
    number_interno = ''
    magazine = ''
    date = ''
    departamento = ''
    proveedor = ''
    razon_social = ''
    cantidad = ''
    precio = 0
    monto = ''
    vendido = ''
    devuelto = ''
    monto_vendido = 0
    subtotal = ''
    total = 0


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
    emitido = False
    impreso = False
#
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
#
class HistoryGuide():
    date = ''
    count_dev = 0
    count_ven = 0
    count_tie = 0
#

def movimientos_by_guia_by_departamento(proveedor, razon_social, departamento):
    """ Funcion que muestra movimiento de guia de proveedor agrupado por departamento"""

    #vriable auxiliar para identificar dia de semana
    DAYS = [
        'LUNES',
        'MARTES',
        'MIERCOLES',
        'JUEVES',
        'VIERNES',
        'SABADO',
        'DOMINGO',
    ]
    #variables que contendra el resultados
    resultado = []
    total = 0
    #verificamos que proveedor y razon_social no sean vacios
    if ((proveedor != '') and (razon_social !='') and (departamento !='')):
        #para el departamento obtenemos movimientos
        #solicitamos consulta
        resultado = Payment.objects.movimientos_by_guia_by_departamento(
            proveedor,
            departamento,
            razon_social
        )

    return resultado

#
def suma_array(array):
    suma = 0
    for a in array:
        suma = suma + a

    return suma
#
def movimientos_by_guia_by_departamento_facturado(proveedor, razon_social, departamento, date):
    """ Funcion que muestra movimiento de guia facturada de proveedor agrupado por departamento"""

    # #variable auxiliar para identificar dia de semana
    # DAYS = [
    #     'LUNES',
    #     'MARTES',
    #     'MIERCOLES',
    #     'JUEVES',
    #     'VIERNES',
    #     'SABADO',
    #     'DOMINGO',
    # ]

    #variables que contendra el resultados
    resultado = []
    #total = 0
    #verificamos que proveedor y razon_social no sean vacios
    if ((proveedor != '') and (razon_social !='')and (razon_social !='') and (date !='')):
        #
        #solicitamos consulta
        queryset = Payment.objects.movimientos_by_guia_by_departamento_facturado(
            proveedor,
            departamento,
            razon_social,
            date
        )
        resultado = queryset
    return resultado
        #variable para sub total
    #     subtotal = 0
    #     # para elemento de la consulta generamos objeto LidacionProveedor
    #     i = 0 #variable para iterar consulta
    #     #
    #     consulta = queryset[0]
    #     #
    #     array_interno = []
    #     while i < consulta.count():
    #         lp = LidacionProveedor() #objeto de datos para template
    #         lp.number = consulta[i]['guia']
    #         print '**********detalle de guia*********'
    #         print consulta[i]['detail_asignation__asignation__detail_guide']
    #         #recuperamos la factura
    #         factura = DetailVoucher.objects.get(
    #             dettail_guide__pk=consulta[i]['detail_asignation__asignation__detail_guide']
    #         )
    #         #completamos lp
    #         lp.factura = factura.voucher.number
    #         lp.number_interno = consulta[i]['facture']
    #         lp.magazine = consulta[i]['magazine'] + ' '+ DAYS[int(consulta[i]['dia'])]
    #         lp.date = consulta[i]['detail_asignation__asignation__detail_guide__guide__date_emission']
    #         lp.departamento = consulta[i]['departamento']
    #         lp.proveedor = consulta[i]['proveedor']
    #         #
    #         if razon_social == '0':
    #             lp.razon_social = 'DPP'
    #         else:
    #             lp.razon_social = 'MAX'
    #         #
    #         lp.cantidad = consulta[i]['detail_asignation__asignation__detail_guide__count']
    #         lp.precio = consulta[i]['detail_asignation__asignation__detail_guide__precio_guia']
    #         lp.monto = lp.cantidad*lp.precio
    #         lp.devuelto = consulta[i]['devuelto']
    #         lp.vendido = lp.cantidad - lp.devuelto
    #         lp.monto_vendido = lp.vendido*lp.precio
    #         total = total + lp.monto_vendido
    #         #agreamos a la lista resultado
    #         resultado.append(lp)
    #
    #         #verificamos que se trata del mismo numero interno
    #         #
    #         if i > 0:
    #             if (resultado[i].number_interno == resultado[i-1].number_interno):
    #                 array_interno.append(lp.monto_vendido)
    #             else:
    #                 resultado[i-1].subtotal = suma_array(array_interno)
    #                 array_interno = [lp.monto_vendido]
    #             #
    #             if i == (consulta.count()-1):
    #                 resultado[i].subtotal = suma_array(array_interno)
    #         else:
    #             array_interno.append(lp.monto_vendido)
    #         i = i + 1
    #
    # return resultado, total


def emitir_boleta(fecha,rs,dep):
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
    consulta = Payment.objects.magazine_boleta(date, rs, dep)

    resultado = []
    for c in consulta:

        if c['count'] > 0:
            itemboleta = ItemBoleta()
            a = str(c['detail_asignation__asignation__detail_guide__guide__date_emission'].year)
            m = str(c['detail_asignation__asignation__detail_guide__guide__date_emission'].month)
            d = str(c['detail_asignation__asignation__detail_guide__guide__date_emission'].day)
            itemboleta.magazine = c['magazine'] +' '+ dias[int(c['dia'])]+"    "+d+"/"+m+"/"+a
            #
            itemboleta.codigo = 'C00'+str(c['detail_asignation__asignation__detail_guide'])
            itemboleta.pk = c['detail_asignation__asignation__detail_guide']
            itemboleta.guide = c['guide']
            itemboleta.date_venta = c['detail_asignation__asignation__detail_guide__guide__date_emission']
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
            if DetailBoleta.objects.filter(detail_guide=detail_guide, boleta__date_venta=date,anulate=False).exists():
                itemboleta.impreso = True
            #itemboleta.emitido =

            resultado.append(itemboleta)

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
        # tienda = Venta.objects.ventas_detail_guide(item.pk)
        hg.count_vendido = res['count_vendido']
        hg.count_deuda = hg.count_deliver - res['count_vendido'] - res['count_devuelto']
        #hg.count_almacen = (item.count - hg.count_deliver) + (res['count_devuelto'] - tienda)
        hg.count_almacen = (
            (item.count - hg.count_deliver) + (res['count_devuelto'])
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

        resultado.append(hg)

    return resultado


# *********************scrips**********************
def actualizar_date_facture_detail_guide():
    #recuperamos toos lo detalle guia en facurado
    detail_guides = DetailGuide.objects.filter(
        anulate=False,
        facturado=True
    )
    #para cada uno actualizmos fecah factura
    for d in detail_guides:
        if Voucher.objects.filter(number_interno=d.facture).exists():
            voucher = Voucher.objects.filter(number_interno=d.facture)[0]
            d.date_facture = voucher.date_emition
            d.save()
            print 'actualizado detalle guia'


def eliminar_detail_voucher():
    details = DetailVoucher.objects.all()
    for d in details:
        if d.voucher.anulate == True:
            d.delete()
            print 'Eliminado Detalle Voucher'
        else:
            print 'No Eliminado'


#funcion que actualiza estado a facturado a guias que no tiene factura
def update_nofacture_detail_guide():
    #
    details = DetailGuide.objects.filter(anulate=False, facturado=True)
    #
    for d in details:
        if DetailVoucher.objects.filter(dettail_guide=d).exists():
            print 'no se actualizo'
        else:
            d.facturado = False
            d.facture = ''
            d.save()
            print '===Estado Cambiado - no se encontro factura==='

    return True
