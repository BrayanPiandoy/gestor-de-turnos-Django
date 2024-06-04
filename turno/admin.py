from django.contrib import admin

from .models import Cliente, Asesor, TipoTramite, Turno

admin.site.register(Cliente)
admin.site.register(Asesor)
admin.site.register(TipoTramite)
admin.site.register(Turno)
