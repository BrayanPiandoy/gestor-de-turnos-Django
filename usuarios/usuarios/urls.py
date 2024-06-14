from django.urls import path
from .views import login_view, registro_view, bienvenido_view, adquirir_turno_view, confirmacion_turno_view

urlpatterns = [
    path('', login_view, name='login'),
    path('registro/<str:numero_cedula>/', registro_view, name='registro'),
    path('bienvenido/<str:numero_cedula>/', bienvenido_view, name='bienvenido'),
    path('adquirir_turno/<str:numero_cedula>/', adquirir_turno_view, name='adquirir_turno'),
    path('confirmacion_turno/<str:numero_cedula>/', confirmacion_turno_view, name='confirmacion_turno'),
]
