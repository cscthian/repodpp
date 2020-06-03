from applications.almacen.recepcion.models import (
    Magazine,
    Guide,
    MagazineDay,
    DetailGuide,
)

from applications.almacen.asignacion.models import DetailAsignation
from applications.caja.pagos.models import Payment
from applications.administrador.models import LostMagazine


#clase que repreenta e objeto inventario
class Inventario():
    pk_diario = ''
    name = ''
    date = ''
    tipo = ''
    cantidad = 0


class Constatar():
    pk_diario = ''
    guia = ''
    name = ''
    count = 0
    real_count = 0
    missing = 0


class Detalle():
    guia = ''
    fecha = ''
    registrado = 0
    entregado = 0
    devuelto = 0
    lost_almacen = 0
    lost_caja = 0
    lost_trasporte = 0
    total = 0

#funcion para listar guias en inventario
def magazine_inventario(detail_guides):
    resul = []
    magazins = []
    resultado = []
    #calculamos el stok de cada uno
    for d in detail_guides:
        aux, devuelto = Payment.objects.salida_magazine(d.pk)
        stock = d.count - DetailAsignation.objects.suma_entregado(d) + devuelto
        inventario = Inventario()
        inventario.pk_diario = d.magazine_day.pk
        inventario.name = d.magazine_day
        inventario.date = d.created.date()
        inventario.tipo = d.magazine_day.magazine.tipo
        inventario.cantidad = stock
        resul.append(inventario)

    #     if not d.magazine_day.pk in magazins:
    #         magazins.append(d.magazine_day.pk)
    #
    # #agrupamos por magazineday
    # for m in magazins:
    #     inv = Inventario()
    #     inv.cantidad = 0
    #     for r in resul:
    #         if m == r.pk_diario:
    #             inv.pk_diario = m
    #             inv.name = r.name
    #             inv.tipo = r.tipo
    #             inv.cantidad = inv.cantidad + r.cantidad
    #
    #     resultado.append(inv)

    return resul

#funcion para recuperar guias a constatar
def magazine_constatar(guide):
    #recuperamos la guia para vlidad su existencia
    guia = Guide.objects.get(number=guide)
    #recuperamos los detalles de la guia
    detail_guides = DetailGuide.objects.filter(
        anulate=False,
        culmined=False,
        guide=guia,
    )
    resultado = []
    #calculamos el stok y devolvemos objeto cosntatar
    for d in detail_guides:
        aux, devuelto = Payment.objects.salida_magazine(d.pk)
        stock = d.count - DetailAsignation.objects.suma_entregado(d) + devuelto
        const = Constatar()
        const.pk_diario = d.magazine_day.pk
        const.guia = d.guide
        const.name = d.magazine_day
        const.count = stock
        const.real_count = stock
        const.missing = 0
        resultado.append(const)

    return resultado


#funcion que devulve el detalle de un magazine day
def magazine_detalle(magazine):
    #recuperamos los detalles de la guia
    detail_guides = DetailGuide.objects.filter(
        anulate=False,
        culmined=False,
        magazine_day__pk=magazine,
    ).order_by('-created')
    resultado = []
    #calculamos el stok y devolvemos objeto cosntatar
    for d in detail_guides:
        detalle = Detalle()
        detalle.guia = d.guide
        detalle.fecha = d.created
        detalle.registrado = d.count
        detalle.entregado = DetailAsignation.objects.suma_entregado(d)
        aux, devuelto = Payment.objects.salida_magazine(d.pk)
        detalle.devuelto = devuelto
        detalle.lost_almacen = LostMagazine.objects.suma_perdidas_module('0',d)
        detalle.lost_caja = LostMagazine.objects.suma_perdidas_module('1',d)
        detalle.lost_trasporte = LostMagazine.objects.suma_perdidas_module('2',d)
        perdidas = detalle.lost_almacen + detalle.lost_caja + detalle.lost_trasporte
        detalle.total = detalle.registrado - detalle.entregado + detalle.devuelto - perdidas
        resultado.append(detalle)

    return resultado
