# -*- encoding: utf-8 -*-
from django import forms

from applications.almacen.recepcion.models import Guide, DetailGuide

class DevolutionForm(forms.Form):
    '''
    formulario para terminar el ciclo de vida de una guia
    '''
    guide = forms.ModelMultipleChoiceField(
        queryset=None,
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        super(DevolutionForm, self).__init__(*args, **kwargs)
        # recuperamos la lista de guias
        guias = Guide.objects.filter(
            anulate=False,
            returned=False,
        ).order_by('created')[:10]
        self.fields['guide'].queryset = guias
        self.fields['guide'].label_from_instance = \
            lambda obj: "%s * %s * %s * %s" % (
                obj.pk,
                obj.number,
                obj.provider,
                obj.date,
            )
