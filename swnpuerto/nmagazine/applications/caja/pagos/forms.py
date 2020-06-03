# -*- encoding: utf-8 -*-
from django import forms

from .models import Caja

class CajaForm(forms.ModelForm):

    class Meta:
        model = Caja
        fields = (
            'real_amount',
        )

        widgets = {
            'real_amount': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                }
            ),
        }

    def clean_real_amount(self):
        amount = self.cleaned_data['real_amount']
        if amount < 0:
            raise forms.ValidationError("Ingrese un monto valido")

        return amount
