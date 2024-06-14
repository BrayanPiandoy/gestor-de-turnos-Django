from django.db import models

class Cliente(models.Model):
    numero_cedula = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    contraseña = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'


class Turno(models.Model):
    TIPO_TURNO_CHOICES = [
        ('documentos', 'Documentos'),
        ('caja', 'Caja'),
        ('asesorias', 'Asesorías'),
        ('servicios', 'Servicios'),
    ]
    
    numero_cedula = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    tipo_turno = models.CharField(max_length=20, choices=TIPO_TURNO_CHOICES)
    numero_turno = models.CharField(max_length=10, unique=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.numero_turno} - {self.nombre} {self.apellido}"
