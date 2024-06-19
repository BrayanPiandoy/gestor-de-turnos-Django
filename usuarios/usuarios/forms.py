from django import forms
from .models import Cliente, Turno

class ClienteRegistroForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['numero_cedula', 'nombre', 'apellido']
        
class ClienteLoginForm(forms.Form):
    numero_cedula = forms.CharField(max_length=20)
    
class AdquirirTurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['tipo_turno']
        widgets = {
            'tipo_turno': forms.Select(choices=Turno.TIPO_TURNO_CHOICES, attrs={'class': 'form-control'}),
        }