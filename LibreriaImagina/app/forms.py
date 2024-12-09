from django import forms
from .models import Contacto, PagoTarjeta
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime
from django.core.exceptions import ValidationError
import re

class ContactoForm(forms.ModelForm):

    class Meta:
        model = Contacto
        fields = '__all__'

class CustomUserCreationForm(UserCreationForm):
    pass

class PagoForm(forms.ModelForm):
    
    class Meta:
        model = PagoTarjeta
        fields = '__all__'

# def run_validator(value):
#     if not re.match(r'^\d{8}-\d$', value):
#         raise ValidationError('El formato del RUT debe ser "XXXXXXXX-X".')
    
# def tel_validator(value):
#     if not re.match(r'^\d{9}$', value):
#         raise ValidationError('El número de teléfono debe tener 9 dígitos')

class ClienteForm(forms.Form):
    nombre_cli = forms.CharField(max_length=15)
    apellido_cli = forms.CharField(max_length=15)
    run = forms.CharField(max_length=15)
    # run = forms.CharField(max_length=15, validators=[run_validator])
    email = forms.EmailField(max_length=30)
    # telefono = forms.CharField(validators=[tel_validator])
    telefono = forms.CharField()
    direccion = forms.CharField(max_length=50)
    contrasena = forms.CharField(max_length=100, widget=forms.PasswordInput)

    def run_validator(self):
        telefono = self.cleaned_data['telefono']
        if not re.match(r'^\d{9}$', telefono):
            raise forms.ValidationError('El número de teléfono debe tener 9 dígitos')
        return telefono

    def tel_validator(self):
        run = self.cleaned_data['run']
        if not re.match(r'^\d{8}-\d$', run):
            raise forms.ValidationError('El formato del RUT debe ser "XXXXXXXX-X"')
        return run