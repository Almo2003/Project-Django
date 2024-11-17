from django.db import models

class Persona(models.Model):
    nombre = models.CharField(max_length=100)
    documento = models.CharField(max_length=20, unique=True)
    programa = models.CharField(max_length=100)
    fechagrado = models.DateField()
    
    def _str_(self):
        return self.nombre


class Trazabilidad(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='trazabilidades')
    ubicacion_laboral = models.CharField(max_length=200, blank=True, null=True)
    correoelectronico = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    oferta = models.CharField(max_length=200, blank=True, null=True)
    fecha_modificacion = models.DateTimeField(auto_now_add=True)
    
    def _str_(self):
        return f"Trazabilidad de {self.persona.nombre}"


            
