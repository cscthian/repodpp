#python
import decimal
#app recepcion
from applications.recepcion.models import DetailGuide, Guide
#app miscelanea
from applications.miscelanea.models import Provider, Departamento
#
from applications.caja.models import Payment
#
from .models import DetailVoucher, Voucher, NotaCredito

#obetos auxiliares

class FacturaNotaCredito():
    facture = None
    venta = 0
    nota = 0
    diferencia = 0


def guias_por_item(q,r,s,t):
    """ funcion que devuelve lista de guais por item"""

    if (s != ''):
        s = Provider.objects.get(pk=s,disable=False).name
    else:
        s = ''
    #
    if (t != ''):
        t = Departamento.objects.get(pk=t).name
    else:
        t = ''
    #recuperamos guias
    consulta, monto_total = DetailGuide.objects.search_item_date_guide(q,r,s,t)

    return consulta,monto_total

def facturas_sin_nota():
    #variabel que cuenta valor
    res = []
    #recuperamos las facturas aun no canceladas
    facturas = Voucher.objects.filter(
        anulate=False,
        state=False,
    )
    #
    for f in facturas:
        #
        sum_notas = NotaCredito.objects.amount_nota_by_facture(f.number_interno)
        #
        sum_ventas = Payment.objects.ventas_by_vocher_factura(f.number_interno)
        #
        suma = float(sum_notas) + float(sum_ventas)
        diferencia =  float(f.amount) - suma
        #
        if not (diferencia < 1):
            fc = FacturaNotaCredito()
            fc.facture = f
            fc.venta = sum_ventas
            fc.nota = sum_notas
            fc.diferencia = diferencia
            res.append(fc)

    return res

# def vouchers_no_payment():
#     #recuperamos factura guia
#     guias =

# *************scrips auxiliares*************+
def actualizar_guide_state():
    guias = Guide.objects.all()
    for g in guias:
        g.facturado = False
        g.save()

    #
    guides = DetailVoucher.objects.all()
    for guide in guides:
        guide.guide.facturado = True
        guide.guide.save()
    return True
