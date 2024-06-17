from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from  usuarios.models import Cliente
from .forms import AreaSelectionForm, AsesorCreationForm, AsesorLoginForm
from .models import Asesor, AsesorArea, TurnoAtendido, TurnoPendiente

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
                    return redirect('select_area')
                else:
                    form.add_error(None, 'Cuenta inactiva')
            else:
                form.add_error(None, 'Credenciales incorrectas')
    else:
        form = AsesorLoginForm()
    return render(request, 'asesores/login.html', {'form': form})


@login_required
def select_area(request):
    if request.method == 'POST':
        form = AreaSelectionForm(request.POST)
        if form.is_valid():
            area = form.cleaned_data['area']
            AsesorArea.objects.update_or_create(asesor=request.user, defaults={'area': area})
            return redirect('ver_turnos_pendientes')
    else:
        form = AreaSelectionForm()
    return render(request, 'asesores/select_area.html', {'form': form})


def ver_turnos_pendientes(request):
    asesor_area = get_object_or_404(AsesorArea, asesor=request.user)
    turnos_pendientes = TurnoPendiente.objects.filter(area=asesor_area.area, estado='pendiente').order_by('fecha_hora')
    return render(request, 'asesores/turnos_pendientes.html', {'turnos': turnos_pendientes, 'area': asesor_area.area})


def cambiar_estado_turno(request, turno_pendiente_id):
    turno_pendiente = get_object_or_404(TurnoPendiente, pk=turno_pendiente_id)

    if request.method == 'POST':
        # Cambiar el estado del turno pendiente a 'atendido'
        turno_pendiente.estado = 'atendido'
        turno_pendiente.save()

        # Crear un registro en TurnoAtendido con la información del turno pendiente
        TurnoAtendido.objects.create(
            asesor=turno_pendiente.asesor,
            cliente=Cliente.objects.get(numero_cedula=turno_pendiente.cliente_cedula),
            area=turno_pendiente.area,
            estado='atendido',
            fecha_hora=turno_pendiente.fecha_hora
        )

        # Eliminar el turno pendiente después de crear el turno atendido
        turno_pendiente.delete()

        # Redirigir a la página de confirmación o a la lista de turnos pendientes
        return redirect('ver_turnos_pendientes')  # Ajusta esto según tu aplicación

    # Si la solicitud no es POST, renderiza el formulario o la página correspondiente
    return render(request, 'asesores/turnos_pendientes.html', {'turno_pendiente': turno_pendiente})


