# Importa el módulo de administración de Django
from django.contrib import admin

# Importa los modelos Persona, Trazabilidad, Egresado e Imagen desde el archivo models.py
from .models import Persona, Trazabilidad, Egresado, Imagen

# Registra el modelo Persona en el administrador de Django
@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    # Especifica los campos que se mostrarán en la lista del administrador
    list_display = ('id', 'nombre', 'documento')
    # Permite buscar registros basados en el campo 'documento'
    search_fields = ('documento',)

# Registra el modelo Trazabilidad en el administrador de Django
@admin.register(Trazabilidad)
class TrazabilidadAdmin(admin.ModelAdmin):
    # Especifica los campos que se mostrarán en la lista del administrador
    list_display = ('id', 'fecha_modificacion', 'ubicacion_laboral', 'correoelectronico', 'telefono', 'oferta')
    # Permite buscar registros basados en el campo 'documento' de la relación con Persona
    search_fields = ('persona__documento',)

# Registra el modelo Egresado en el administrador de Django
@admin.register(Egresado)
class EgresadoAdmin(admin.ModelAdmin):
    # Especifica los campos que se mostrarán en la lista del administrador
    list_display = (
        'id', 
        'nombre', 
        'profesion', 
        'ano_grado', 
        'cargo_actual', 
        'correo', 
        'descripcion', 
        'trayectoria', 
        'datos_adicionales', 
        'Imagen'
    )

    # Sobrescribe el método save_model para agregar una validación personalizada
    def save_model(self, request, obj, form, change):
        # Restringe la cantidad de registros del modelo Egresado a un máximo de 3
        if Egresado.objects.count() >= 3:
            raise ValueError("No puedes agregar más de 3 egresados.")
        # Llama al método original de la clase padre para guardar el objeto
        super().save_model(request, obj, form, change)

# Registra el modelo Imagen en el administrador de Django
@admin.register(Imagen)
class ImagenAdmin(admin.ModelAdmin):
    # Especifica los campos que se mostrarán en la lista del administrador
    list_display = ('id', 'nombre', 'imagen')
