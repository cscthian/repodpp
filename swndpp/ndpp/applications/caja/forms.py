# -*- encoding: utf-8 -*-
from django import forms


class LiquidacionDiaForm(forms.Form):
    '''
        formulario para filtrar lisquidacion por dia
    '''
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
