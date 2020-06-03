# -*- encoding: utf-8 -*-
from django import forms

from .models import Provider, Vendor

#creamos los formularios

class ProviderForm(forms.ModelForm):

    class Meta:
        model = Provider
        fields = (
            'ruc',
            'name',
            'phone',
            'email',
        )

        widgets = {
            'ruc': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'placeholder': 'Ingrese el ruc del proveedor'
                }
            ),
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'placeholder': 'Ingrese el nombre para el proveedor'
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'placeholder': 'Ingrese telefono o celular'
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'placeholder': 'Ingrese email de proveedor'
                }
            ),
        }

    def clean_ruc(self):
        ruc = self.cleaned_data['ruc']
        if not ruc.isdigit():
            raise forms.ValidationError("Ingrese solo numeros por favor")
        elif len(ruc) < 11:
            raise forms.ValidationError("El ruc debe 11 digitos")
        return ruc

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 4:
            raise forms.ValidationError("nombre demasiado corto")
        return name


class VendorForm(forms.ModelForm):

    class Meta:
        model = Vendor
        fields = (
            'cod',
            'dni',
            'name',
            'seudonimo',
            'type_vendor',
            'line_credit',
            'plazo',
        )
        widgets = {
            'cod': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'placeholder': 'Ingrese el Codigo'
                }
            ),
            'dni': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'placeholder': 'Ingrese el dni'
                }
            ),
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'placeholder': 'Ingrese el Nombre completo'
                }
            ),
            'seudonimo': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'placeholder': 'Ingrese un seudonimo'
                }
            ),
            'type_vendor':forms.Select(
                attrs={
                    'class': 'form-control input-sm'
                }
            ),
            'line_credit': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '0.0',
                    'size': '16',
                }
            ),
            'plazo': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '0',
                    'size': '16',
                }
            )
        }

    def clean_dni(self):
        dni = self.cleaned_data['dni']
        if not dni.isdigit():
            raise forms.ValidationError("Ingrese solo numeros por favor")
        elif len(dni) < 8:
            raise forms.ValidationError("El dni debe 8 digitos")
        return dni

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 4:
            raise forms.ValidationError("nombre demasiado corto")
        return name
