# -*- encoding: utf-8 -*-

from rest_framework import serializers

#applications reportes
from applications.reportes.models import DetailVoucher, Voucher, NotaCredito

#app pagos
from applications.caja.models import Payment
#
from .models import PaymentVoucher

class ListFacturaSerializer(serializers.ModelSerializer):
    """ serializador para listar facturas """

    responsabilidad = serializers.SerializerMethodField()
    voucher = serializers.CharField(source='id')
    monto_factura = serializers.SerializerMethodField()
    amount_nota = serializers.SerializerMethodField()
    correcto = serializers.BooleanField(default=False)


    def get_responsabilidad(self,obj):
        return '0'

    def get_monto_factura(self,obj):
        print obj.number_interno
        return Payment.objects.ventas_by_vocher_factura(obj.number_interno)

    def get_amount_nota(self,obj):
        return NotaCredito.objects.amount_nota_by_facture(obj.number_interno)


    class Meta:
        model = Voucher
        fields = (
            'voucher',
            'number',
            'number_interno',
            'date_emition',
            'amount',
            'monto_factura',
            'amount_nota',
            'state',
            'responsabilidad',
            'correcto',
        )


class PagoFacturaSerializer(serializers.Serializer):
    """serializador para registrar pagos de factura"""

    factura = serializers.CharField()
    codigo_pago = serializers.CharField()
    responsabilidad = serializers.CharField()
    date_pago = serializers.DateField(required=False)
    monto_real = serializers.DecimalField(
        max_digits=10,
        decimal_places=3,
        required=False
    )


class BoletaSerializer(serializers.Serializer):
    """ serializador para listar items de boleta """
    pk = serializers.CharField()
    total = serializers.DecimalField(max_digits=10, decimal_places=3)
    codigo = serializers.CharField()
    magazine = serializers.CharField()
    number = serializers.CharField()
    client = serializers.CharField()
    date_emition = serializers.DateField()
    date_venta = serializers.DateField()
    count = serializers.IntegerField()
    precio_venta = serializers.DecimalField(max_digits=10, decimal_places=3)
    precio_sunat = serializers.DecimalField(max_digits=10, decimal_places=3)
    amount = serializers.DecimalField(max_digits=10, decimal_places=3)
    afecto = serializers.BooleanField()
    addressee = serializers.CharField()
    vendor = serializers.CharField(required=False)
    emitido = serializers.BooleanField()
    impreso = serializers.BooleanField()


class BoletaSaveSerializer(serializers.Serializer):
    """ serializador para guardar items de boleta """

    total = serializers.DecimalField(max_digits=10, decimal_places=3)
    detail_guide = serializers.CharField()
    number = serializers.CharField()
    client = serializers.CharField()
    date_emition = serializers.DateField()
    date_venta = serializers.DateField()
    count = serializers.IntegerField()
    precio_venta = serializers.DecimalField(max_digits=10, decimal_places=3)
    precio_sunat = serializers.DecimalField(max_digits=10, decimal_places=3)
    amount = serializers.DecimalField(max_digits=10, decimal_places=3)
    afecto = serializers.BooleanField()
    addressee = serializers.CharField()


class CuadreVentaSerializer(serializers.Serializer):
    """ serializador reporte de fecha en lapso de fechas """

    detail_guide = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    precio = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    guia = serializers.CharField()
    magazine = serializers.CharField()
    total = serializers.DecimalField(max_digits=10, decimal_places=3)
    proveedor = serializers.CharField()
    devuelto = serializers.IntegerField()
    pagado = serializers.IntegerField()
    dia = serializers.CharField()

    def get_detail_guide(self,obj):
        return obj['detail_asignation__asignation__detail_guide']

    def get_date(self,obj):
        return obj['detail_asignation__asignation__detail_guide__guide__date']

    def get_precio(self,obj):
        return obj['detail_asignation__asignation__detail_guide__precio_unitario']

    def get_count(self,obj):
        return obj['detail_asignation__asignation__detail_guide__count']


class MontosFaltantesSerializer(serializers.ModelSerializer):
    """ serializador para listar perdidas por area"""

    guia = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()
    date_facture = serializers.SerializerMethodField()
    monto_deuda = serializers.DecimalField(max_digits=10, decimal_places=3, default=0)
    responsabilidad = serializers.SerializerMethodField()
    pk = serializers.CharField(source='id')


    def get_guia(self,obj):
        res = []
        details = DetailVoucher.objects.filter(voucher=obj.factura)
        for d in details:
            res.append(d.dettail_guide.guide.number)
        return res

    def get_items(self,obj):
        res = []
        details = DetailVoucher.objects.filter(voucher=obj.factura)
        for d in details:
            res.append(d.dettail_guide.magazine_day.magazine.name)
        return res

    def get_date_facture(self,obj):
        return obj.factura.date_emition

    def get_responsabilidad(self,obj):
        return str(obj.get_responsabilidad_display())


    class Meta:
        model = PaymentVoucher
        fields = (
            'pk',
            'factura',
            'codigo_pago',
            'date_pago',
            'monto_real',
            'monto_factura',
            'responsabilidad',
            'items',
            'guia',
            'date_facture',
            'monto_deuda',
        )


class ResetMontosFaltantesSerializer(serializers.Serializer):
    """ reinicia los faltantes """

    pk = serializers.CharField()



class LiquidacionProveedorReporteSerialier(serializers.Serializer):
    """ serializador reporte de compra total """

    total = serializers.SerializerMethodField()
    deuda = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    guia = serializers.CharField()
    proveedor = serializers.CharField()
    departamento = serializers.CharField()
    cantidad = serializers.IntegerField()
    precio = serializers.DecimalField(max_digits=10, decimal_places=3, default=0)
    devuelto = serializers.IntegerField()
    pagado = serializers.IntegerField()
    magazine = serializers.CharField()
    dia = serializers.SerializerMethodField()

    def get_total(self,obj):
        return obj['precio']*obj['cantidad']

    def get_deuda(self,obj):
        return obj['cantidad'] - obj['devuelto'] - obj['pagado']

    def get_subtotal(self,obj):
        return (obj['cantidad'] - obj['devuelto'])*obj['precio']

    def get_dia(self,obj):
        DAYS = [
            'LUN',
            'MAR',
            'MIE',
            'JUE',
            'VIE',
            'SAB',
            'DOM',
        ]
        return DAYS[int(obj['dia'])]

    def get_date(self,obj):
        return obj['detail_asignation__asignation__detail_guide__guide__date_emission']


class LiquidacionFacturaProveedorReporteSerialier(serializers.Serializer):
    """ serializador reporte de compra facturada """

    total = serializers.SerializerMethodField()
    deuda = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()
    monto = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    dia = serializers.SerializerMethodField()
    facture = serializers.CharField()
    guia = serializers.CharField()
    proveedor = serializers.CharField()
    departamento = serializers.CharField()
    cantidad = serializers.IntegerField()
    precio = serializers.DecimalField(max_digits=10, decimal_places=3, default=0)
    devuelto = serializers.IntegerField()
    pagado = serializers.IntegerField()
    magazine = serializers.CharField()

    def get_total(self,obj):
        return obj['precio']*obj['cantidad']

    def get_deuda(self,obj):
        return obj['cantidad'] - obj['devuelto'] - obj['pagado']

    def get_subtotal(self,obj):
        return (obj['cantidad'] - obj['devuelto'])*obj['precio']

    def get_dia(self,obj):
        DAYS = [
            'LUN',
            'MAR',
            'MIE',
            'JUE',
            'VIE',
            'SAB',
            'DOM',
        ]
        return DAYS[int(obj['dia'])]

    def get_date(self,obj):
        return obj['detail_asignation__asignation__detail_guide__guide__date_emission']

    def get_monto(self,obj):
        return ''
