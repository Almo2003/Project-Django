from django.db import models

class Persona(models.Model):
    nombre = models.CharField(max_length=200)
    documento = models.IntegerField(max_length=15, default=0000000000)
    programa = models.CharField(max_length=100, default='PROGRAMAS')
    fechagrado = models.DateField(default='2000-01-01')
    ubicacion_laboral = models.CharField(max_length=200, default='lugar')
    correoelectronico = models.EmailField(blank=False, null=True)
    telefono = models.IntegerField(max_length=20, default=0000000000)
    oferta = models.CharField(max_length=500)


    def __str__(self):
        return (
            f"{self.nombre} "
            f"{self.documento} "
            f"{self.programa} "
            f"{self.fechagrado} "
            f"{self.ubicacion_laboral} "
            f"{self.correoelectronico} "
            f"{self.telefono} "
            f"{self.oferta}"
        )