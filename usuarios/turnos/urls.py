from django.urls import path
from .views import gestion_turnos, cargar_turnos

urlpatterns = [
    path('', gestion_turnos, name='gestion_turnos'),
    path('cargar_turnos/', cargar_turnos, name='cargar_turnos'),
]
