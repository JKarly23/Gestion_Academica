from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from estudiantes.models import Estudiante
from profesor.models import Profesor


# Create your models here.

class Asignatura(models.Model):
    name = models.CharField(max_length=50)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, null=True,blank=True,related_name="profesor")
    
    
    def __str__(self) -> str:
        return self.name


class ComentarioAsignatura(models.Model):
    tema = models.TextField()
    create = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name="estudiante_comentario")
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE, related_name="comentario_asignatura")

    def __str__(self) -> str:
        return self.tema
    
class Nota(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    profesor =models.ForeignKey(Profesor, on_delete=models.CASCADE)
    nota = models.FloatField(validators=[MinValueValidator(2,"El numero introducido esta fuera de rango"), MaxValueValidator(5,"El numero introducido esta fuera de rango")])
    

    def __str__(self) -> str:
        return  str(self.nota)

