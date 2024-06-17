from datetime import datetime
from asesores.models import TurnoPendiente
from .forms import ClienteRegistroForm, ClienteLoginForm, AdquirirTurnoForm
from .models import Cliente,Turno
from django.shortcuts import render, redirect, get_object_or_404
from usuarios.models import Cliente  # Importar el modelo Cliente
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

def adquirir_turno_view(request, numero_cedula):
    cliente = get_object_or_404(Cliente, numero_cedula=numero_cedula)
    asesor = request.user  # Suponiendo que el asesor está logueado y es el usuario actual
    
    if request.method == 'POST':
        form = AdquirirTurnoForm(request.POST)
        if form.is_valid():
            turno = form.save(commit=False)
            turno.numero_cedula = cliente.numero_cedula
            turno.nombre = cliente.nombre
            turno.apellido = cliente.apellido
            turno.fecha_hora = datetime.now()  # Asignar la fecha y hora actuales

            # Generar número de turno único
            letra_turno = turno.tipo_turno[0].upper()
            ultimo_turno = Turno.objects.filter(tipo_turno=turno.tipo_turno).order_by('fecha_hora').last()
            numero_secuencial = int(ultimo_turno.numero_turno[1:]) + 1 if ultimo_turno else 1
            turno.numero_turno = f"{letra_turno}{numero_secuencial}"
            
            turno.save()

            # Crear una entrada en la tabla TurnoPendiente
            TurnoPendiente.objects.create(
                asesor=asesor,
                cliente_cedula=cliente.numero_cedula,
                nombre_cliente=cliente.nombre,
                apellido_cliente=cliente.apellido,
                area=turno.tipo_turno,
                estado='pendiente',
                fecha_hora=turno.fecha_hora
            )

            return redirect('confirmacion_turno', numero_cedula=turno.numero_cedula)
    else:
        form = AdquirirTurnoForm()
    
    return render(request, 'turnos/adquirir_turno.html', {'form': form})



def confirmacion_turno_view(request, numero_cedula):
    turno = get_object_or_404(Turno, numero_cedula=numero_cedula)
    return render(request, 'turnos/confirmacion_turno.html', {'turno': turno, 'numero_cedula': numero_cedula})

