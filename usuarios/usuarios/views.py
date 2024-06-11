from django.shortcuts import render, redirect
from .forms import ClienteRegistroForm, ClienteLoginForm
from .models import Cliente
import re

def login_view(request):
    if request.method == 'POST':
        form = ClienteLoginForm(request.POST)
        if form.is_valid():
            numero_cedula = form.cleaned_data['numero_cedula']
            # Validar que el número de cédula sea numérico y tenga de 8 a 10 dígitos
            if re.match(r'^\d{8,10}$', numero_cedula):
                try:
                    cliente = Cliente.objects.get(numero_cedula=numero_cedula)
                    return redirect('bienvenido', numero_cedula=numero_cedula)
                except Cliente.DoesNotExist:
                    return redirect('registro', numero_cedula=numero_cedula)
            else:
                form.add_error('numero_cedula', 'El número de cédula debe tener entre 8 y 10 dígitos numéricos.')
    else:
        form = ClienteLoginForm()
    return render(request, 'usuarios/login.html', {'form': form})

def registro_view(request, numero_cedula):
    if request.method == 'POST':
        form = ClienteRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bienvenido', numero_cedula=numero_cedula)
    else:
        form = ClienteRegistroForm(initial={'numero_cedula': numero_cedula})
    return render(request, 'usuarios/registro.html', {'form': form})


def bienvenido_view(request, numero_cedula):
    cliente = Cliente.objects.get(numero_cedula=numero_cedula)
    return render(request, 'usuarios/bienvenido.html', {'cliente': cliente})