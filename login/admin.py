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
    list_display = ('id', 
                    'nombre', 
                    'profesion', 
                    'ano_grado', 
                    'cargo_actual', 
                    'correo', 
                    'descripcion', 
                    'trayectoria', 
                    'datos_adicionales', 
                    'imagen_url')

    def save_model(self, request, obj, form, change):
        if Egresado.objects.count() >= 3:
            raise ValueError("No puedes agregar más de 3 egresados.")
        super().save_model(request, obj, form, change)
