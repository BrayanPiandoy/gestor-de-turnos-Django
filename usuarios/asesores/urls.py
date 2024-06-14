# asesores/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.login_view, name='login_asesor'),
    path('login_asesor/', views.login_view, name='login_asesor'),
    path('pagina_asesor/', views.pagina_asesor, name='pagina_asesor'),
]
