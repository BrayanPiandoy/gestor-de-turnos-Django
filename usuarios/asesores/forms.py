from django import forms

from usuarios.models import Turno
from .models import Asesor

class AsesorCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput)

    class Meta:
        model = Asesor
        fields = ('cedula', 'name', 'last_name')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class AsesorLoginForm(forms.Form):
    cedula = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class AreaSelectionForm(forms.Form):
    area = forms.ChoiceField(choices=Turno.TIPO_TURNO_CHOICES, required=True)
