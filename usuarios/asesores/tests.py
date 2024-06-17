from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.middleware import SessionMiddleware
from django.test.client import RequestFactory
from django.contrib.auth.models import AnonymousUser
from asesores.models import TurnoPendiente, TurnoAtendido
from usuarios.models import Cliente
from asesores.views import cambiar_estado_turno


class CambiarEstadoTurnoTestCase(TestCase):
    def setUp(self):
        # Crear un usuario asesor para simular la sesión
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='12345')
        
        # Crear un cliente
        self.cliente = Cliente.objects.create(numero_cedula='1004215230', nombre='Juan', apellido='Perez')
        
        # Crear un turno pendiente para el test
        self.turno_pendiente = TurnoPendiente.objects.create(
            asesor=self.user,
            cliente_cedula=self.cliente.numero_cedula,
            nombre_cliente=self.cliente.nombre,
            apellido_cliente=self.cliente.apellido,
            area='Consulta',
            estado='pendiente',
            fecha_hora=timezone.now()
        )
        
        # Agregar permisos al usuario asesor para acceder a la vista cambiar_estado_turno
        content_type = ContentType.objects.get_for_model(TurnoPendiente)
        permission = Permission.objects.get(content_type=content_type, codename='change_turnopendiente')
        self.user.user_permissions.add(permission)
        
        # Configurar la request factory
        self.factory = RequestFactory()
        
    def test_cambiar_estado_turno(self):
        # Crear una solicitud POST con la sesión de usuario simulada
        url = reverse('cambiar_estado_turno', args=[self.turno_pendiente.pk])
        request = self.factory.post(url)
        request.user = self.user
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        
        # Ejecutar la vista
        response = cambiar_estado_turno(request, turno_pendiente_id=self.turno_pendiente.pk)
        
        # Verificar que la respuesta sea una redirección (código 302)
        self.assertEqual(response.status_code, 302)
        
        # Verificar que el estado del turno pendiente haya cambiado a 'atendido'
        turno_pendiente_actualizado = TurnoPendiente.objects.get(pk=self.turno_pendiente.pk)
        self.assertEqual(turno_pendiente_actualizado.estado, 'atendido')
        
        # Verificar que se haya creado un turno atendido con la información correcta
        turno_atendido = TurnoAtendido.objects.get(asesor=self.user, cliente=self.cliente)
        self.assertEqual(turno_atendido.area, self.turno_pendiente.area)
        self.assertEqual(turno_atendido.estado, 'atendido')
        self.assertEqual(turno_atendido.fecha_hora, self.turno_pendiente.fecha_hora)
        
        # Verificar que el turno pendiente se haya eliminado
        with self.assertRaises(TurnoPendiente.DoesNotExist):
            TurnoPendiente.objects.get(pk=self.turno_pendiente.pk)
