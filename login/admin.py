from django.contrib import admin
from .models import Persona

class PersonaAdmin(admin.ModelAdmin):
    list_display = ('id' , 'nombre' , 'documento')  # Solo los campos de Persona

admin.site.register(Persona, PersonaAdmin)

    
