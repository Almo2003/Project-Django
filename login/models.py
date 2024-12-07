from django.db import models

class Persona(models.Model):
    nombre = models.CharField(max_length=100)
    documento = models.CharField(max_length=20, unique=True)
    programa = models.CharField(max_length=100)
    fechagrado = models.DateField()
    
    def __str__(self):
        return self.nombre


class Trazabilidad(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='trazabilidades')
    ubicacion_laboral = models.CharField(max_length=200, blank=True, null=True)
    correoelectronico = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    oferta = models.CharField(max_length=200, blank=True, null=True)
    fecha_modificacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return (
            f"Trazabilidad de {self.persona.nombre} - "
            f"Ubicación: {self.ubicacion_laboral or 'N/A'}, "
            f"Correo: {self.correoelectronico or 'N/A'}, "
            f"Teléfono: {self.telefono or 'N/A'}, "
            f"Oferta: {self.oferta or 'N/A'}, "
            f"Fecha: {self.fecha_modificacion.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        
class Egresado(models.Model):
    nombre = models.CharField(max_length=100)
    profesion = models.CharField(max_length=100)
    ano_grado = models.IntegerField()
    cargo_actual = models.CharField(max_length=100)
    correo = models.EmailField()
    descripcion = models.TextField()
    trayectoria = models.TextField()
    datos_adicionales = models.TextField()
    imagen = models.ImageField(upload_to='egresados/', blank=True, null=True)

    def __str__(self):
        return self.nombre


            
