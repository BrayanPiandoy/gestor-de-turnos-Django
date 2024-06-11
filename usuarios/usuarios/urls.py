from django.urls import path
from .views import login_view, registro_view, bienvenido_view

urlpatterns = [
    path('', login_view, name='login'),
    path('registro/<str:numero_cedula>/', registro_view, name='registro'),
    path('bienvenido/<str:numero_cedula>/', bienvenido_view, name='bienvenido'),
]
