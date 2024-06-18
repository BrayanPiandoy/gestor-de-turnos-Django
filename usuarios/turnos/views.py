from django.shortcuts import render
from django.http import JsonResponse
from asesores.models import TurnoPendiente, TurnoAtendido

def gestion_turnos(request):
    return render(request, 'gestion_turnos/vista_principal.html')

def cargar_turnos(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        turnos_pendientes = list(TurnoPendiente.objects.all().values())
        turnos_atendidos = list(TurnoAtendido.objects.all().values())
        data = {
            'turnos_pendientes': turnos_pendientes,
            'turnos_atendidos': turnos_atendidos,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Método de solicitud incorrecto'}, status=400)
