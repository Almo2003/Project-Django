from django.contrib import admin
from .models import Persona, Trazabilidad, Egresado

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'documento')
    search_fields = ('documento',)

@admin.register(Trazabilidad)
class TrazabilidadAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha_modificacion', 'ubicacion_laboral', 'correoelectronico', 'telefono', 'oferta')
    search_fields = ('persona__documento',)

@admin.register(Egresado) 
class EgresadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre' , 'profesion' , 'ano_grado' , 'cargo_actual' , 'correo' , 'descripcion' , 'trayectoria' , 'datos_adicionales' , 'imagen')
