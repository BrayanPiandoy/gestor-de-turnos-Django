from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import AsesorCreationForm, AsesorLoginForm
from .models import Asesor

def register(request):
    if request.method == 'POST':
        form = AsesorCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_asesor')
    else:
        form = AsesorCreationForm()
    return render(request, 'asesores/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AsesorLoginForm(request.POST)
        if form.is_valid():
            cedula = form.cleaned_data.get('cedula')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=cedula, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('pagina_asesor')
                else:
                    form.add_error(None, 'Cuenta inactiva')
            else:
                form.add_error(None, 'Credenciales incorrectas')
    else:
        form = AsesorLoginForm()
    return render(request, 'asesores/login.html', {'form': form})

@login_required
def pagina_asesor(request):
    return render(request, 'asesores/pagina_asesores.html')
