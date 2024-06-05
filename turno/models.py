from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AbstractUser



OPCIONES_ESTADO = [
    ('REALIZADO', 'Realizado'),
    ('PENDIENTE', 'Pendiente')
]

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    turno = models.OneToOneField('Turno', on_delete=models.SET_NULL, null=True, blank=True, related_name='cliente_turno')

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    

class TipoTramite(models.Model):
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return self.descripcion
    

class Turno(models.Model):
    cliente = models.OneToOneField('Cliente', on_delete=models.CASCADE, related_name='turno_cliente')
    asesor = models.ForeignKey(User, on_delete=models.CASCADE)
    tramite = models.ForeignKey('TipoTramite', on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=OPCIONES_ESTADO)

    def __str__(self):
        return f"Turno {self.id} - {self.estado} - {self.cliente} - {self.asesor}"
    

