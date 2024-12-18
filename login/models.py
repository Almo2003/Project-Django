# Importa el módulo models de Django para definir los modelos
from django.db import models

# Modelo para representar una persona
class Persona(models.Model):
    # Campo para almacenar el nombre de la persona
    nombre = models.CharField(max_length=100)
    # Campo único para el documento de identificación
    documento = models.CharField(max_length=20, unique=True)
    # Campo para el programa académico de la persona
    programa = models.CharField(max_length=100)
    # Campo para la fecha de grado
    fechagrado = models.DateField()
    
    # Método para representar el objeto como una cadena (usado en el administrador y consultas)
    def __str__(self):
        return self.nombre  # Devuelve el nombre de la persona como su representación

# Modelo para registrar la trazabilidad de una persona
class Trazabilidad(models.Model):
    # Relación con el modelo Persona, elimina las trazabilidades si se elimina la persona
    persona = models.ForeignKey(
        Persona, 
        on_delete=models.CASCADE, 
        related_name='trazabilidades'  # Nombre de la relación inversa en consultas
    )
    # Campos para información relacionada con la trazabilidad, todos opcionales
    ubicacion_laboral = models.CharField(max_length=200, blank=True, null=True)
    correoelectronico = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    oferta = models.CharField(max_length=200, blank=True, null=True)
    # Fecha automática de creación del registro
    fecha_modificacion = models.DateTimeField(auto_now_add=True)
    
    # Método para representar el objeto como una cadena con un resumen de los datos
    def __str__(self):
        return (
            f"Trazabilidad de {self.persona.nombre} - "
            f"Ubicación: {self.ubicacion_laboral or 'N/A'}, "
            f"Correo: {self.correoelectronico or 'N/A'}, "
            f"Teléfono: {self.telefono or 'N/A'}, "
            f"Oferta: {self.oferta or 'N/A'}, "
            f"Fecha: {self.fecha_modificacion.strftime('%Y-%m-%d %H:%M:%S')}"
        )

# Modelo para representar un egresado
class Egresado(models.Model):
    # Campo para el nombre del egresado, con un valor predeterminado
    nombre = models.CharField(max_length=100, default="Sin nombre")
    # Campo para almacenar la imagen del egresado, se guarda en la carpeta 'egresado/'
    Imagen = models.ImageField(upload_to='egresado/')
    # Campos para información adicional del egresado
    profesion = models.CharField(max_length=100)
    ano_grado = models.IntegerField()  # Año de graduación
    cargo_actual = models.CharField(max_length=100)
    correo = models.EmailField()  # Correo electrónico
    descripcion = models.TextField()  # Descripción breve del egresado
    trayectoria = models.TextField()  # Detalle de la trayectoria del egresado
    datos_adicionales = models.TextField()  # Información adicional
    
    # Método para representar el objeto como una cadena
    def __str__(self):
        return self.nombre  # Devuelve el nombre del egresado como su representación

# Modelo para representar una imagen independiente
class Imagen(models.Model):
    # Campo para la imagen, se guarda en la carpeta 'multimedia/'
    imagen = models.ImageField(upload_to='multimedia/')
    # Campo para el nombre de la imagen
    nombre = models.CharField(max_length=255)
    
    # Método para representar el objeto como una cadena
    def __str__(self):
        # Devuelve el nombre de la imagen si existe, o un texto predeterminado
        return self.nombre if self.nombre else "Imagen sin nombre"
