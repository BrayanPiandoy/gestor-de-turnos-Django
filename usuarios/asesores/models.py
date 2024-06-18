from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from usuarios.models import Cliente, Turno
from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings

class AsesorManager(BaseUserManager):
    def create_user(self, cedula, name, last_name, password=None):
        if not cedula:
            raise ValueError('El usuario debe tener una cédula')
        user = self.model(
            cedula=cedula,
            name=name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cedula, name, last_name, password):
        user = self.create_user(
            cedula,
            password=password,
            name=name,
            last_name=last_name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Asesor(AbstractBaseUser):
    cedula = models.CharField(max_length=20, unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = AsesorManager()

    USERNAME_FIELD = 'cedula'
    REQUIRED_FIELDS = ['name', 'last_name']

    def __str__(self):
        return f'{self.name} {self.last_name} ({self.cedula})'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    

class AsesorArea(models.Model):
    asesor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    area = models.CharField(max_length=20, choices=Turno.TIPO_TURNO_CHOICES)

    def __str__(self):
        return f'{self.asesor} - {self.get_area_display()}'



class TurnoPendiente(models.Model):
    asesor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cliente_cedula = models.CharField(max_length=20, validators=[MinLengthValidator(8)], verbose_name='Cédula del Cliente')
    nombre_cliente = models.CharField(max_length=100, verbose_name='Nombre del Cliente')
    apellido_cliente = models.CharField(max_length=100, verbose_name='Apellido del Cliente')
    area = models.CharField(max_length=20, choices=Turno.TIPO_TURNO_CHOICES)
    estado = models.CharField(max_length=20, default='pendiente')
    numero_turno = models.CharField(max_length=10)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nombre_cliente} {self.apellido_cliente} - {self.area} ({self.fecha_hora})'


class TurnoAtendido(models.Model):
    asesor = models.ForeignKey(Asesor, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    area = models.CharField(max_length=20, choices=Turno.TIPO_TURNO_CHOICES)
    estado = models.CharField(max_length=20, default='atendido')
    fecha_hora = models.DateTimeField()
    numero_turno = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.cliente.numero_cedula} - {self.get_area_display()} - {self.estado}'

