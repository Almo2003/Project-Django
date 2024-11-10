# models.py
from django.db import models

class Persona(models.Model):
    nombre = models.CharField(max_length=200)
    documento = models.IntegerField(unique=True)
    programa = models.CharField(max_length=100)
    fechagrado = models.DateField()

    def __str__(self):
        return f"{self.nombre} - {self.documento} - {self.programa} - {self.fechagrado}"

class Trasabilidad(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name="trasabilidad")
    telefono = models.CharField(max_length=15)
    correoelectronico = models.EmailField()
    ubicacion_laboral = models.TextField()  # Para almacenar múltiples ubicaciones si es necesario
    oferta = models.TextField()  # Para registrar múltiples ofertas de trabajo si es necesario
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    def agregar_nuevo_telefono(self, nuevo_telefono):
        if nuevo_telefono not in self.telefono.split(", "):
            self.telefono += f", {nuevo_telefono}" if self.telefono else nuevo_telefono
            self.save()
            
    def agregar_nuevo_correoelectronico(self, nuevo_correoelectronico):
        if nuevo_correoelectronico not in self.correoelectronico.split(", "):
            self.correoelectronico += f", {nuevo_correoelectronico}" if self.correoelectronico else nuevo_correoelectronico
            self.save()

    def agregar_nueva_ubicacion_laboral(self, nueva_ubicacion_laboral):
        if nueva_ubicacion_laboral not in self.ubicacion_laboral.split(", "):
            self.ubicacion_laboral += f", {nueva_ubicacion_laboral}" if self.ubicacion_laboral else nueva_ubicacion_laboral
            self.save()

    def agregar_nueva_oferta(self, nueva_oferta):
        if nueva_oferta not in self.oferta.split(", "):
            self.oferta += f", {nueva_oferta}" if self.oferta else nueva_oferta
            self.save()

    def __str__(self):
        return f"{self.persona.nombre} - Historial"
