from django.shortcuts import render, get_object_or_404, redirect
from .models import Cliente, Turno
from .forms import ClienteForm, TurnoForm


def index(request):
    return render(request,'index.html')

# --------------Turnos------------

def lista_turnos(request):
    turnos = Turno.objects.all()
    return render(request, 'turno/lista_turnos.html', {'turnos': turnos})

def detalle_turno(request, pk):
    turno = get_object_or_404(Turno, pk=pk)
    return render(request, 'turnos/detalle_turno.html', {'turno': turno})

def crear_turno(request):
    if request.method == "POST":
        form = TurnoForm(request.POST)
        if form.is_valid():
            turno = form.save()
            return redirect('detalle_turno', pk=turno.pk)
    else:
        form = TurnoForm()
    return render(request, 'turnos/editar_turno.html', {'form': form})

def editar_turno(request, pk):
    turno = get_object_or_404(Turno, pk=pk)
    if request.method == "POST":
        form = TurnoForm(request.POST, instance=turno)
        if form.is_valid():
            form.save()
            return redirect('detalle_turno', pk=pk)
    else:
        form = TurnoForm(instance=turno)
    return render(request, 'turnos/editar_turno.html', {'form': form})

# --------------clientes------------

def crear_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            return redirect('detalle_cliente', pk=cliente.pk)
    else:
        form = ClienteForm()
    return render(request, 'clientes/edit_cliente.html', {'form': form})

def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('detalle_cliente', pk=pk)
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'turnos/editar_cliente.html', {'form': form})

def detalle_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    clientes = Cliente.objects.all()
    return render(request, 'clientes/detail_cliente.html', {'cliente': cliente})

def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/list_clientes.html', {'clientes': clientes})