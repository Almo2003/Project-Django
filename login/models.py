from django.db import models

class Persona(models.Model):
    nombre = models.CharField(max_length=200)
    documento = models.IntegerField(default=0000000000)
    programa = models.CharField(max_length=100, default='PROGRAMAS')
    fechagrado = models.DateField(default='16-06-2021')
    ubicacion_laboral = models.CharField(max_length=200, default='lugar')
    correoelectronico = models.EmailField(blank=False, null=True)
    telefono = models.IntegerField(default=0000000000)
    oferta = models.CharField(max_length=500 , default='oferta academica')


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


class Trazabilidad(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='trazabilidades')
    ubicacion_laboral = models.CharField(max_length=100)
    correoelectronico = models.EmailField()
    telefono = models.CharField(max_length=20)
    oferta = models.CharField(max_length=200)
    fecha_modificacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Trazabilidad de {self.persona.nombre} - {self.fecha_modificacion}"

            
