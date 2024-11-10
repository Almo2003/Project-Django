from django.contrib import admin
from .models import Persona, Trasabilidad

class PersonaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'documento', 'programa', 'fechagrado')  # Solo los campos de Persona

class TrasabilidadAdmin(admin.ModelAdmin):
    list_display = ('persona', 'telefono', 'correoelectronico', 'ubicacion_laboral', 'oferta', 'fecha_modificacion')  # Campos de Trasabilidad

admin.site.register(Persona, PersonaAdmin)
admin.site.register(Trasabilidad, TrasabilidadAdmin)
    
