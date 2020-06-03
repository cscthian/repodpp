# -*- encoding: utf-8 -*-
from django import forms

#app miscelanea
from applications.miscelanea.models import Provider, Departamento

#app rececpcion
from applications.recepcion.models import DetailGuide, Guide

from .models import Voucher, NotaCredito


class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class SearchGuideForm(forms.Form):
    '''
        formulario para buscar guia
    '''
    item = forms.CharField(
        label='Nombre Producto',
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Buscar por ...',
            }
        )
    )
    date = forms.CharField(
        label='Fecha de registro',
        max_length=10,
        required=False,
        widget=forms.TextInput(
            attrs={
                'type': 'date',
            }
        )
    )
    provider = forms.ModelChoiceField(
        queryset=None,
        required=False,
    )
    departamento = MyModelChoiceField(
        queryset=Departamento.objects.all(),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(SearchGuideForm, self).__init__(*args, **kwargs)
        self.fields['provider'].queryset = Provider.objects.filter(
            disable=False,
        )


class SearchVoucherForm(forms.Form):
    '''
        formulario para buscar Facturas
    '''
    number = forms.CharField(
        label='Numero de Factura',
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Numero de Factura...',
            }
        )
    )


class VoucherForm(forms.ModelForm):
    """ formulario para registrar voucher """

    class Meta:
        model = Voucher
        fields = (
            'type_voucher',
            'number',
            'date_emition',
            'date_due',
            'number_interno',
            'igv',
            'amount',
        )

        widgets = {
            'number': forms.TextInput(
                attrs={
                    'placeholder': 'Numero de Factura'
                }
            ),
            'number_interno': forms.TextInput(
                attrs={
                    'placeholder': 'Numero de Interno'
                }
            ),
            'reference': forms.TextInput(
                attrs={
                    'placeholder': 'Referencia'
                }
            ),
            'date_emition': forms.TextInput(
                attrs={
                    'type':'date'
                }
            ),
            'date_due': forms.TextInput(
                attrs={
                    'type':'date'
                }
            ),
        }

    def clean_number(self):
        number = self.cleaned_data['number']
        if Voucher.objects.filter(number=number,anulate=False).exists():
            msj = 'El Numero de Factura ya Existe'
            print msj
            self.add_error('number', msj)
        else:
            return number

    def clean_number_interno(self):
        number = self.cleaned_data['number_interno']
        if Voucher.objects.filter(number_interno=number,anulate=False).exists():
            msj = 'El Codigo interno ya exite'
            print msj
            self.add_error('number_interno', msj)
        else:
            return number


class VoucherUpdateForm(forms.ModelForm):
    """ formulario para modificar voucher """
    class Meta:
        model = Voucher
        fields = (
            'date_emition',
            'date_due',
            'number_interno',
            'igv',
            'amount',
        )

        widgets = {
            'number_interno': forms.TextInput(
                attrs={
                    'placeholder': 'Numero de Interno'
                }
            ),
            'reference': forms.TextInput(
                attrs={
                    'placeholder': 'Referencia'
                }
            ),
            'date_emition': forms.TextInput(
                attrs={
                    'type':'date'
                }
            ),
            'date_due': forms.TextInput(
                attrs={
                    'type':'date'
                }
            ),
        }


class NotaCreditoForm(forms.ModelForm):
    """ formulario para registrar Nota de Credito """

    class Meta:
        model = NotaCredito
        fields = (
            'number',
            'date_emition',
            'reference',
            'amount',
        )

        widgets = {
            'number': forms.TextInput(
                attrs={
                    'placeholder': 'Numero de Nota de credito'
                }
            ),
            'reference': forms.TextInput(
                attrs={
                    'placeholder': 'Referencia'
                }
            ),
            'date_emition': forms.TextInput(
                attrs={
                    'type':'date'
                }
            ),
            'amount': forms.NumberInput(
                attrs={
                    'placeholder': 'Monto: 2000',
                }
            ),
        }
