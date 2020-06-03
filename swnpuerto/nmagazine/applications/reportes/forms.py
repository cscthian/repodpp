# -*- encoding: utf-8 -*-
from django import forms
from .models import CierreMes


class CierreForm(forms.ModelForm):

    class Meta:
        model = CierreMes
        fields = (
            'mes',
            'date_start',
            'date_end',
            'venta_neta_real',
            'ingreso_neto_real',
        )
        widgets = {
            'mes':forms.Select(
                attrs={
                    'class': 'form-control input-sm'
                }
            ),
            'date_start': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'id':'datetimepicker1',
                    'type':'date',
                    'ng-model':'vm.fecha1',
                    'ata-date-format':'DD-MM-YYYY',
                },
            ),
            'date_end': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'id':'datetimepicker1',
                    'type':'date',
                    'ng-model':'vm.fecha2',
                    'ata-date-format':'DD-MM-YYYY',
                    'ng-change':'vm.consulta_montos(vm.fecha1,vm.fecha2)'
                },
            ),
            'venta_neta_real': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'ng-model':'vm.venta_real'
                }
            ),
            'ingreso_neto_real': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'ng-model':'vm.ingreso_real'
                }
            ),
        }

    def clean_venta_neta_real(self):
        venta_neta_real = self.cleaned_data['venta_neta_real']
        if venta_neta_real < 0:
            raise forms.ValidationError("Ingrese monto valido")

        return venta_neta_real

    def clean_ingreso_neto_real(self):
        ingreso_neto_real = self.cleaned_data['ingreso_neto_real']
        if ingreso_neto_real < 0:
            raise forms.ValidationError("Ingrese monto valido")

        return ingreso_neto_real

    def clean_date_end(self):
        date_start = self.cleaned_data['date_start']
        date_end = self.cleaned_data['date_end']
        if date_end < date_start:
            raise forms.ValidationError("Ingrese fecha valida")

        return date_end
