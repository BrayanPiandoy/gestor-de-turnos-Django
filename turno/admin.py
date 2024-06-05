from django.contrib import admin

from .models import Cliente, TipoTramite, Turno

admin.site.register(Cliente)
admin.site.register(TipoTramite)
admin.site.register(Turno)
