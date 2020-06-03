# -*- encoding: utf-8 -*-
from django import forms

from .models import Magazine, MagazineDay, Guide, DetailGuide

from applications.almacen.entidad.models import Provider

class MagazineForm(forms.ModelForm):
    '''forulario para registrar un diario'''

    precio_tapa = forms.DecimalField(
        max_digits=10,
        decimal_places=3,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': '0.0',
                'size': '16',
            }
        )
    )
    precio_guia = forms.DecimalField(
        max_digits=10,
        decimal_places=3,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': '0.0',
                'size': '16',
            }
        )
    )
    precio_venta = forms.DecimalField(
        max_digits=10,
        decimal_places=3,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': '0.0',
                'size': '16',
            }
        )
    )
    precio_tapad = forms.DecimalField(
        max_digits=10,
        decimal_places=3,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': '0.0',
                'size': '16',
            }
        )
    )
    precio_guiad = forms.DecimalField(
        max_digits=10,
        decimal_places=3,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': '0.0',
                'size': '16',
            }
        )
    )
    precio_ventad = forms.DecimalField(
        max_digits=10,
        decimal_places=3,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': '0.0',
                'size': '16',
            }
        )
    )
    class Meta:
        model = Magazine
        fields = (
            'name',
            'provider',
            'description',
            'day_expiration',
        )
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre',
                }
            ),
            'description': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Descripcion',
                }
            ),
            'provider': forms.Select(
                attrs={'class': 'form-control input-sm'}
            ),
            'day_expiration': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Dias de Vencimiento',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(MagazineForm, self).__init__(*args, **kwargs)
        self.fields['provider'].queryset = Provider.objects.filter(
            disable=False,
        )

    def clean_precio_tapa(self):
        precio_tapa = self.cleaned_data['precio_tapa']

        if precio_tapa < 0:
            msj = 'no puede tener un precio menor a cero'
            self.add_error('precio_tapa', msj)
        else:
            return precio_tapa

    def clean_precio_guia(self):
        precio_guia = self.cleaned_data['precio_guia']

        if precio_guia < 0:
            msj = 'no puede tener un precio menor a cero'
            self.add_error('precio_guia', msj)
        else:
            return precio_guia

    def clean_precio_venta(self):
        precio_venta = self.cleaned_data['precio_venta']

        if precio_venta < 0:
            msj = 'no puede tener un precio menor a cero'
            self.add_error('precio_venta', msj)
        else:
            return precio_venta

    def clean_precio_tapad(self):
        precio_tapad = self.cleaned_data['precio_tapad']

        if precio_tapad < 0:
            msj = 'no puede tener un precio menor a cero'
            self.add_error('precio_tapad', msj)
        else:
            return precio_tapad

    def clean_precio_guiad(self):
        precio_guiad = self.cleaned_data['precio_guiad']

        if precio_guiad < 0:
            msj = 'no puede tener un precio menor a cero'
            self.add_error('precio_guiad', msj)
        else:
            return precio_guiad

    def clean_precio_ventad(self):
        precio_ventad = self.cleaned_data['precio_ventad']

        if precio_ventad < 0:
            msj = 'no puede tener un precio menor a cero'
            self.add_error('precio_ventad', msj)
        else:
            return precio_ventad


class MagazineUpdateForm(forms.ModelForm):
    '''forulario para modificar un diario'''

    precio_tapa = forms.DecimalField(
        max_digits=10,
        decimal_places=3,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': '0.0',
                'size': '16',
            }
        )
    )
    precio_guia = forms.DecimalField(
        max_digits=10,
        decimal_places=3,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': '0.0',
                'size': '16',
            }
        )
    )
    precio_venta = forms.DecimalField(
        max_digits=10,
        decimal_places=3,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': '0.0',
                'size': '16',
            }
        )
    )

    class Meta:
        model = Magazine
        fields = (
            'name',
            'provider',
            'description',
            'day_expiration',
        )
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre',
                }
            ),
            'description': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Descripcion',
                }
            ),
            'provider': forms.Select(
                attrs={'class': 'form-control input-sm'}
            ),
            'day_expiration': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Dias de Vencimiento',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(MagazineUpdateForm, self).__init__(*args, **kwargs)
        self.fields['provider'].queryset = Provider.objects.filter(
            disable=False,
        )

    def clean_precio_tapa(self):
        precio_tapa = self.cleaned_data['precio_tapa']

        if precio_tapa < 0:
            msj = 'no puede tener un precio menor a cero'
            self.add_error('precio_tapa', msj)
        else:
            return precio_tapa

    def clean_precio_guia(self):
        precio_guia = self.cleaned_data['precio_guia']

        if precio_guia < 0:
            msj = 'no puede tener un precio menor a cero'
            self.add_error('precio_guia', msj)
        else:
            return precio_guia

    def clean_precio_venta(self):
        precio_venta = self.cleaned_data['precio_venta']

        if precio_venta < 0:
            msj = 'no puede tener un precio menor a cero'
            self.add_error('precio_venta', msj)
        else:
            return precio_venta


class ProductAddForm(forms.ModelForm):
    '''forulario para registrar un producto'''

    precio_tapa = forms.DecimalField(
        max_digits=10,
        decimal_places=3,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': '0.0',
                'ng-model':'vm.precio_tapa',
                'ng-change':'vm.calcular_precio(vm.tipo, vm.precio_tapa)',
                'size': '16',
            }
        )
    )
    precio_guia = forms.DecimalField(
        max_digits=10,
        decimal_places=3,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': '0.0',
                'ng-model':'vm.precio_guia',
                'size': '16',
            }
        )
    )
    precio_venta = forms.DecimalField(
        max_digits=10,
        decimal_places=3,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': '0.0',
                'ng-model':'vm.precio_venta',
                'size': '16',
            }
        )
    )
    sponsor = forms.ModelChoiceField(
        queryset=None,
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-control input-sm',
                'placeholder': 'Pulse para Seleccionar',
            }
        ),
    )
    class Meta:
        model = Magazine
        fields = (
            'name',
            'provider',
            'description',
            'day_expiration',
            'code',
            'afecto',
        )
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre',
                }
            ),
            'description': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Descripcion',
                }
            ),
            'provider': forms.Select(
                attrs={'class': 'form-control input-sm'}
            ),
            'day_expiration': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Tiempo de Reparto Dias',
                }
            ),
            'code': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Codigo de Producto',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(ProductAddForm, self).__init__(*args, **kwargs)
        self.fields['provider'].queryset = Provider.objects.filter(
            disable=False,
        )
        self.fields['sponsor'].queryset = Magazine.objects.filter(
            disable=False,
            tipo='0',
        )

    def clean_precio_tapa(self):
        precio_tapa = self.cleaned_data['precio_tapa']

        if precio_tapa < 0:
            msj = 'no puede tener un precio menor a cero'
            self.add_error('precio_tapa', msj)
        else:
            return precio_tapa

    def clean_precio_guia(self):
        precio_guia = self.cleaned_data['precio_guia']

        if precio_guia < 0:
            msj = 'no puede tener un precio menor a cero'
            self.add_error('precio_guia', msj)
        else:
            return precio_guia

    def clean_precio_venta(self):
        precio_venta = self.cleaned_data['precio_venta']

        if precio_venta < 0:
            msj = 'no puede tener un precio menor a cero'
            self.add_error('precio_venta', msj)
        else:
            return precio_venta


class GuideForm(forms.ModelForm):
    """formulario para modificar una guia"""
    class Meta:
        model =Guide
        fields = (
            'number_invoce',
            'date_emission',
            'provider',
            'plazo_return',
        )
        widgets = {
            'number_invoce': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'size':'16',
                    'placeholder': 'Numero Interno',
                }
            ),
            'date_emission': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'datepiker',
                    'placeholder': 'Fecha',
                }
            ),
            'provider': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'plazo_return': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'size':'16',
                    'placeholder': 'Dias de Vencimiento',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(GuideForm, self).__init__(*args, **kwargs)
        self.fields['provider'].queryset = Provider.objects.filter(
            disable=False
        )


    def clean_number_invoce(self):
        number_invoce = self.cleaned_data['number_invoce']
        if not number_invoce.isdigit() or number_invoce < 0:
            msj = 'Solo deben contener numeros'
            self.add_error('number_invoce', msj)
        else:
            return number_invoce


class ProductForm(forms.ModelForm):
    '''forulario para ediatr un producto'''

    precio_tapa = forms.DecimalField(
        max_digits=10,
        decimal_places=3,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': '0.0',
                'size': '16',
            }
        )
    )
    precio_guia = forms.DecimalField(
        max_digits=10,
        decimal_places=3,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': '0.0',
                'size': '16',
            }
        )
    )
    precio_venta = forms.DecimalField(
        max_digits=10,
        decimal_places=3,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': '0.0',
                'size': '16',
            }
        )
    )
    precio_tapad = forms.DecimalField(
        max_digits=10,
        decimal_places=3,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': '0.0',
                'size': '16',
            }
        )
    )
    precio_guiad = forms.DecimalField(
        max_digits=10,
        decimal_places=3,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': '0.0',
                'size': '16',
            }
        )
    )
    precio_ventad = forms.DecimalField(
        max_digits=10,
        decimal_places=3,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': '0.0',
                'size': '16',
            }
        )
    )
    sponsor = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(
            attrs={
                'class': 'form-control input-sm',
                'placeholder': 'Pulse para Seleccionar',
            }
        ),
    )
    class Meta:
        model = Magazine
        fields = (
            'name',
            'provider',
            'description',
            'day_expiration',
            'code',
        )
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre',
                }
            ),
            'description': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Descripcion',
                }
            ),
            'provider': forms.Select(
                attrs={'class': 'form-control input-sm'}
            ),
            'day_expiration': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Dias de Vencimiento',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['provider'].queryset = Provider.objects.filter(
            disable=False,
        )
        self.fields['sponsor'].queryset = Magazine.objects.filter(
            disable=False,
            tipo='0',
        )

    def clean_precio_tapa(self):
        precio_tapa = self.cleaned_data['precio_tapa']

        if precio_tapa < 0:
            msj = 'no puede tener un precio menor a cero'
            self.add_error('precio_tapa', msj)
        else:
            return precio_tapa

    def clean_precio_guia(self):
        precio_guia = self.cleaned_data['precio_guia']

        if precio_guia < 0:
            msj = 'no puede tener un precio menor a cero'
            self.add_error('precio_guia', msj)
        else:
            return precio_guia

    def clean_precio_venta(self):
        precio_venta = self.cleaned_data['precio_venta']

        if precio_venta < 0:
            msj = 'no puede tener un precio menor a cero'
            self.add_error('precio_venta', msj)
        else:
            return precio_venta

    def clean_precio_tapad(self):
        precio_tapad = self.cleaned_data['precio_tapad']

        if precio_tapad < 0:
            msj = 'no puede tener un precio menor a cero'
            self.add_error('precio_tapad', msj)
        else:
            return precio_tapad

    def clean_precio_guiad(self):
        precio_guiad = self.cleaned_data['precio_guiad']

        if precio_guiad < 0:
            msj = 'no puede tener un precio menor a cero'
            self.add_error('precio_guiad', msj)
        else:
            return precio_guiad

    def clean_precio_ventad(self):
        precio_ventad = self.cleaned_data['precio_ventad']

        if precio_ventad < 0:
            msj = 'no puede tener un precio menor a cero'
            self.add_error('precio_ventad', msj)
        else:
            return precio_ventad


class DetailGuideForm(forms.ModelForm):

    class Meta:
        model = DetailGuide
        fields = (
            'magazine_day',
            'count',
        )

    def __init__(self, *args, **kwargs):
        super(DetailGuideForm, self).__init__(*args, **kwargs)
        self.fields['magazine_day'].queryset = MagazineDay.objects.filter(
            magazine__disable=False
        )

    def clean_count(self):
        count = self.cleaned_data['count']
        if count < 0:
            msj = 'Ingrese un numero valido'
            self.add_error('count', msj)
        else:
            return count
