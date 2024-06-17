# asesores/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.login_view, name='login_asesor'),
    path('login_asesor/', views.login_view, name='login_asesor'),
    path('select_area/', views.select_area, name='select_area'),
    path('turnos_pendientes/', views.ver_turnos_pendientes, name='ver_turnos_pendientes'),
    path('cambiar_estado_turno/<int:turno_pendiente_id>/', views.cambiar_estado_turno, name='cambiar_estado_turno'),
]
