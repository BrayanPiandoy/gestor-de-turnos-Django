from django import forms
from .models import Cliente

class ClienteRegistroForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['numero_cedula', 'nombre', 'apellido', 'contraseña']
        widgets = {
            'contraseña': forms.PasswordInput(),
        }

class ClienteLoginForm(forms.Form):
    numero_cedula = forms.CharField(max_length=20)