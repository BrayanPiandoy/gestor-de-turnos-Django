from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

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
    

