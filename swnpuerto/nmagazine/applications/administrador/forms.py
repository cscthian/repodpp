# -*- encoding: utf-8 -*-
from django import forms


class NotaForm(forms.Form):
    '''formulario para nota de credito'''
    guide = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Numero de Guia',
                'class':'form-control',
                'size':'16',
                'ng-model':'vm.guide',
                'ng-change':'vm.listar_items(vm.guide)',
            }
        )
    )
    magazine_day = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'codigo de guias',
                'class':'form-control',
                'size':'16',
                'ng-model':'vm.magazine',
            }
        )
    )
    precio_guia = forms.DecimalField(
        max_digits=10,
        decimal_places=3,
        widget=forms.NumberInput(
            attrs={
                'placeholder': '0.00',
                'class':'form-control',
                'size':'16',
                'ng-model':'vm.precio_guia',
            }
        )
    )
    precio_venta = forms.DecimalField(
        max_digits=10,
        decimal_places=3,
        widget=forms.NumberInput(
            attrs={
                'placeholder': '0.00',
                'class':'form-control',
                'size':'16',
                'ng-model':'vm.precio_venta',
            }
        )
    )
