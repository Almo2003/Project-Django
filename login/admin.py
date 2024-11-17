from django.contrib import admin
from .models import Persona, Trazabilidad

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'documento')
    search_fields = ('documento',)

@admin.register(Trazabilidad)
class TrazabilidadAdmin(admin.ModelAdmin):
    list_display = ('persona', 'fecha_modificacion', 'ubicacion_laboral', 'correoelectronico', 'telefono', 'oferta')
    search_fields = ('persona__documento',)

    
