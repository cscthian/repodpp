# -*- encoding: utf-8 -*-
from django import forms

#app miscelanea
from applications.miscelanea.models import Provider, Departamento


class FilterForm(forms.Form):
    '''
        formulario para buscar guia o factura
    '''

    CHOICES = (
        ('0', 'Todo'),
        ('1', 'Cerradas'),
        ('2', 'No Cerradas'),
    )
    date_start = forms.CharField(
        label='Fecha de registro',
        max_length=10,
        required=False,
        widget=forms.TextInput(
            attrs={
                'type': 'date',
            }
        )
    )
    date_end = forms.CharField(
        label='Fecha de registro fin',
        max_length=10,
        required=False,
        widget=forms.TextInput(
            attrs={
                'type': 'date',
            }
        )
    )
    number = forms.CharField(
        label='Numero',
        max_length=10,
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Numero...',
            }
        )
    )
    state = forms.ChoiceField(choices=CHOICES)


class ProviderLiquidacionForm(forms.Form):
    """ formulario para liquidacion de guias """
    CHOICES_RS = (
        ('0', 'DPP'),
        ('1', 'MAX'),
    )
    razon_social = forms.ChoiceField(choices=CHOICES_RS)
    provider = forms.ModelChoiceField(
        queryset=Provider.objects.filter(disable=False),
        required=False,
    )
    departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        required=False,
    )


class FilterProviderLiquidacion(forms.Form):
    '''
        formulario filtrar liquidacion
    '''

    CHOICES = (
        ('0', 'DPP'),
        ('1', 'MAX'),
    )

    rs = forms.ChoiceField(choices=CHOICES)
    date = forms.DateField(
        'Fecha',
        required=False,
        widget=forms.DateInput(
            attrs={
                'type': 'date',
            },
            format='%d/%m/%Y'
        )
    )
    provider = forms.ModelChoiceField(
        queryset=Provider.objects.filter(disable=False),
        required=False,
    )
    departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        required=False,
    )


class BoletaFilterForm(forms.Form):
    '''
        formulario para buscar boletas
    '''

    date_emition = forms.CharField(
        label='Fecha de emision',
        max_length=10,
        required=False,
        widget=forms.TextInput(
            attrs={
                'type': 'date',
                'class': 'input-group-field',
            }
        )
    )


class SearchGuidesForm(forms.Form):
    '''
        formulario para buscar guia
    '''

    kword = forms.CharField(
        label='Numero',
        max_length=10,
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Numero...',
            }
        )
    )
