from django.contrib import admin
from .models import Persona

class PersonaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'documento', 'programa', 'fechagrado', 'ubicacion_laboral', 'correoelectronico', 'telefono', 'oferta')

admin.site.register(Persona, PersonaAdmin)
    
