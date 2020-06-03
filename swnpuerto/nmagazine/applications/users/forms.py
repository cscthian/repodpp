# -*- encoding: utf-8 -*-
from django import forms
# from .models import User

from django.contrib.auth import authenticate

from .models import User

class LoginForm(forms.Form):

    username = forms.CharField(
        label='usuario',
        max_length='30',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'username',
                'autofocus': 'autofocus',
                'size': '16',
            }
        ),
    )
    password = forms.CharField(
        label='contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'password',
                'size': '16',
            }
        ),
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not authenticate(username=username, password=password):
            raise forms.ValidationError('username o password incorrectos.')
        return self.cleaned_data


class UserForm(forms.ModelForm):

    password1 = forms.CharField(
        label='contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control input-sm',
                'placeholder': 'Ingrese una contraseña'
            }
        ),
    )
    password2 = forms.CharField(
        label='contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control input-sm',
                'placeholder': 'repetir la contraseña'
            }
        ),
    )

    class Meta:
        model = User
        fields = (
            'username',
            'type_user',
        )
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'placeholder': 'username'
                }
            ),
            'type_user': forms.Select(
                attrs={
                    'class': 'form-control input-sm',
                }
            ),
        }

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'las contraseñas no coinciden..!!')
        elif len(password2) < 5:
            print 'menor a 5 caracteres'
            self.add_error(
                'password2',
                'la contraseña debe tener por lo menos 5 caracteres!!'
            )
        else:
            return password2



class UserUpdateForm(forms.ModelForm):

    password1 = forms.CharField(
        label='contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control input-sm',
                'placeholder': 'Ingrese una contraseña'
            }
        ),
    )
    password2 = forms.CharField(
        label='contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control input-sm',
                'placeholder': 'repetir la contraseña'
            }
        ),
    )

    class Meta:
        model = User
        fields = (
            'type_user',
        )
        widgets = {
            'type_user': forms.Select(
                attrs={
                    'class': 'form-control input-sm',
                }
            ),
        }

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'las contraseñas no coinciden..!!')
        elif len(password2) < 5:
            print 'menor a 5 caracteres'
            self.add_error(
                'password2',
                'la contraseña debe tener por lo menos 5 caracteres!!'
            )
        else:
            return password2
