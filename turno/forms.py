from django import forms
from .models import Cliente, Turno, TipoTramite
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'email', 'telefono']

class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['cliente', 'asesor', 'tramite', 'fecha_hora', 'estado']
        

class LoginForm(AuthenticationForm):
    pass

class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['cliente', 'tramite', 'fecha_hora']